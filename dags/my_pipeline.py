from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime
import os

host_path = os.environ.get('HOST_PWD')

#Define the defaults

default_args = {
	'start_date': datetime(2026,3,1),
	'auto_remove': 'success'
}

#Define the DAG

with DAG(
	"commodity-tracker-pipeline",
	default_args = default_args,
	schedule = '*/15 * * * *',
	catchup = False,
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
		entrypoint = ["python", "scripts/get-price.py"],
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
		entrypoint = ["python", "scripts/data_loader.py"],
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

check_db_status >> extract >> load