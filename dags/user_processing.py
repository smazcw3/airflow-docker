from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator

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


# Define the DAG
with DAG('user_processing', start_date=datetime(2024, 1, 1), 
         schedule_interval='@daily', catchup=False) as dag:
    '''
    A DAG consists of tasks and those tasks are defined as operators
    An operator is one task in our data pipeline
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
    which is why we can add dependencies as shown below
    '''
    extract_user >> process_user



    

