from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator, Mount
from datetime import datetime

# define the default args

default_args = {
    'start_date': datetime(2026,1,1),
    'auto_remove': 'success'
}

# Define the DAG

with DAG(
    "docker-basics",
    default_args =  default_args,
    schedule = '@hourly',
    catchup = False,
) as dag:
    
    #first element of DAG

    check_status = DockerOperator(
        task_id = 'checking_docker',
        image = 'hello-world',
        )

    run_command = DockerOperator (
        task_id = 'run_command',
        image = 'alpine:latest',
        command = 'date',)

    #create the workflow

    check_status >> run_command

with DAG('05_three_tasks',
    default_args = default_args,
    schedule = None,
    catchup = False,
) as dag:

    write = DockerOperator(
        task_id='write_file',
        image='alpine:latest',
        command=['sh', '-c', 'echo "Hello from first" > /data/message.txt'],
        mounts=[Mount(source='./data',
                      target='/data',
                      type='bind')],
    )

    read = DockerOperator(
        task_id='read_file',
        image='alpine:latest',
        command=['cat', '/data/message.txt'],
         mounts=[Mount(source='./data',  # same path
                  target='/data',
                  type='bind')],
    )


    check_db = DockerOperator(
        task_id='check_db',
        image='postgres:14',
        command=['pg_isready', '-h', 'postgres', '-U', 'myuser'],
        environment={'PGPASSWORD': 'secret'},
        # network='etl-network',
        
    )

    write >> read >> check_db