from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
 
from datetime import datetime
 
#We can share data between tasks using xcom
#xcom stands for "Cross communication" and it allows to exchange small amounts of data
#between tasks
def _t1(ti):
    #ti is the task instance of your task allowing us to
    #access the method xcom_push.
    #When an operator runs, it creates a task instance
    ti.xcom_push(key="my_key", value=42)
 
def _t2(ti):
    #To pull the xcom data from task t1 to task t2
    print(ti.xcom_pull(key="my_key", task_ids='t1'))

def _branch(ti):
    value = ti.xcom_pull(key="my_key", task_ids='t1')
    if (value == 42):
        return 't2'
    return 't3'
 
with DAG("xcom_dag", start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:
 
    t1 = PythonOperator(
        task_id='t1',
        python_callable=_t1
    )

    branch = BranchPythonOperator(
        task_id='branch',
        python_callable=_branch
    )
 
    t2 = PythonOperator(
        task_id='t2',
        python_callable=_t2
    )
 
    t3 = BashOperator(
        task_id='t3',
        bash_command="echo ''"
    )

    t4 = BashOperator(
        task_id='t4',
        bash_command="echo ''",
        trigger_rule='none_failed_min_one_success' #Will trigger t4 with t2 suceeded and regardless of t3
    )
 
    t1 >> branch >> [t2, t3] >> t4