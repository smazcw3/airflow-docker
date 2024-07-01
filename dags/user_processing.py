from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from pandas import json_normalize
import json
from datetime import datetime

def _process_user(ti):
    """
    This function is to process the user information output from "extrac_user" task
    and save it as csv file.
    """
    user = ti.xcom_pull(task_ids="extract_user")
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

def _store_user():
    hook = PostgresHook(postgres_conn_id="postgres")
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ','",
        filename="/tmp/processed_user.csv"
    )

# Define the DAG
with DAG('user_processing', start_date=datetime(2024, 1, 1), 
         schedule_interval='@daily', catchup=False) as dag:
    '''
    A DAG consists of tasks and those tasks are defined as operators
    An operator is one task in our data pipeline.
    @param schedule_interval: It defined how a DAG should run from the start_date + schedule_time 

    There are 3 types of operator:
    1. Action operator: Executes an action
    2. Transfer operator: Transfer data
    3. Sensors: Waiting for a condition to be met
    
    Now, lets create an operator to create a table. With create_table, we would use postGres operator to 
    execute a SQL request against a PostGRes database and create a table
    '''
    create_table = PostgresOperator(task_id='create_table',
                                    postgres_conn_id='postgres',
                                    sql='''
                                    CREATE TABLE IF NOT EXISTS users(
                                    firstName TEXT NOT NULL,
                                    lastName TEXT NOT NULL,
                                    country TEXT NOT NULL,
                                    username TEXT NOT NULL,
                                    password TEXT NOT NULL,
                                    email TEXT NOT NULL
                                    );
                                    '''
                                   )
    

    '''
    We can now think of creating sensors. A sensor waits for something to happen before moving to the next task 
    For example, we can check whether an API is available or not and for that we can create an HTTPSensor
    '''
    is_api_available = HttpSensor(task_id="is_api_available",
                                  http_conn_id="user_api",
                                  endpoint="api/"
                                 )
    
    '''
    We can now define an http operators that extracts the user information from the user_api we created
    '''
    extract_user = SimpleHttpOperator(task_id="extract_user", 
                                      http_conn_id="user_api", 
                                      endpoint="/api", 
                                      method="GET", 
                                      response_filter=lambda response: json.loads(response.text)
                                     )
    
    '''
    Once we have extracted the user, we can now process the user using Python operator
    '''
    process_user = PythonOperator(task_id="process_user", 
                                  python_callable=_process_user
                                 )


    '''
    Make sure that extract_user task run is preceded by process_user
    which is why we can add dependencies as
    
    extract_user >> process_user
    '''

    '''
    Lets make use of hooks. A hook is used for interacting with external tools. 
    An operator makes use of external tool or service through hooks. 
    For example, if we have a Postgres operator then it can interact with a Postgres database by running an SQL query through a Postgres "hook".
    The purpose, here for the hook it to abstract all the complexities of interacting with a postgres database.
    '''
    store_user = PythonOperator(task_id="store_user", 
                                python_callable=_store_user
                               )
    '''
    Now, its time to declare all the dependencies within tasks
    '''
    create_table >> is_api_available >> extract_user >> process_user >> store_user