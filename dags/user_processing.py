from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime

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


    

