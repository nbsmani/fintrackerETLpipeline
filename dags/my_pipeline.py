import os
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

#get the project_root_directory from env vars
host_path = os.environ.get('HOST_PWD')

#Define the defaults

default_args = {
	'start_date': datetime(2026,3,1),
	'retries' : 3,
	'auto_remove': 'success'
}

#Define the DAG

with DAG(
	"commodity-tracker-pipeline",
	default_args = default_args,
	schedule = '*/15 * * * *',  #Crypto markets are 24/7, so we can run the pipeline every 15 minutes all day
	catchup = False,
	template_searchpath = ['/opt/airflow/scripts'],
	max_active_runs = 1,
	) as dag:

	check_db_status = DockerOperator(
		task_id = 'check_db_status',
		image = 'postgres:14',
		command=['pg_isready','-h','postgres','-U','myuser'],
		environment={'PGPASSWORD': 'secret'},
		network_mode='commodity-price-tracker_etl-network')


	extract = DockerOperator(
		task_id = 'extract_commodity_prices',
		image = 'cpd-python',
		entrypoint = ["python", "scripts/extract/get-price.py"],
		mounts = [
		#data_dir	
			Mount(source=f'{host_path}/data',
       			  target='/commodity-tracker/data',
       			  type= "bind"),
		#Scripts dir
			Mount(source=f'{host_path}/scripts',
				  target='/commodity-tracker/scripts',
				  type="bind")],
		network_mode = 'commodity-price-tracker_etl-network',)

	load = DockerOperator(
		task_id = 'load_commodity_prices_to_bronze',
		image = 'cpd-python',
		entrypoint = ["python", "scripts/load/load-data.py"],
		mounts = [
		#dataDir
			Mount(source=f'{host_path}/data',
       			  target='/commodity-tracker/data',
       			  type= "bind"),
		#Scripts dir
			Mount(source=f'{host_path}/scripts',
				  target='/commodity-tracker/scripts',
				  type="bind")],
		network_mode = 'commodity-price-tracker_etl-network',

		command = ["/commodity-tracker/data/landing_zone/",
              "myuser", #user name of the db 
              "secret", #password of the db
              "postgres", #db service name, ipaddress resolved by DNS
              "5432", #port where the db service is exposed
              "commodity_db", #database name
              "bronze", #schema name
              "bronze_prices", #table name
              "/commodity-tracker/data/archive/"])

	silver_ddl = SQLExecuteQueryOperator(
		task_id = "ddl_for_silver",
		conn_id = "postgres_default",
		sql = "sql/silver/ddl_silver.sql")


	promote_to_silver = SQLExecuteQueryOperator(
		task_id = "promote_bronze_to_silver",
		conn_id = "postgres_default",
		sql = "sql/silver/promote_to_silver.sql")

	gold_ddl = SQLExecuteQueryOperator(
		task_id = "ddl_for_gold",
		conn_id = "postgres_default",
		sql = "sql/gold/ddl_gold.sql")

	promote_to_gold = SQLExecuteQueryOperator(
		task_id = "promote_silver_to_gold",
		conn_id = "postgres_default",
		sql = "sql/gold/promote_to_gold.sql")

check_db_status >> extract >> load >> silver_ddl >> promote_to_silver >> gold_ddl >> promote_to_gold

