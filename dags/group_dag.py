from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.subdag import SubDagOperator
#from subdags.subdag_downloads import subdag_downloads
#from subdags.subdag_transforms import subdag_transforms
from groups.group_downloads import download_tasks
from groups.group_transforms import transform_tasks
 
from datetime import datetime
 
with DAG('group_dag', start_date=datetime(2022, 1, 1), 
    schedule_interval='@daily', catchup=False) as dag:

    args = {'start_date': dag.start_date, 'schedule_interval': dag.schedule_interval, 'catchup': dag.catchup}
 
    ## We can group the download tasks into the "downloads" task using TaskGoup instead of Subdags
    downloads = download_tasks()

    # ## We can group the download tasks into one "downloads" task
    # downloads = SubDagOperator(
    #     task_id='downloads', 
    #     subdag=subdag_downloads(dag.dag_id, 'downloads', args))

    # download_a = BashOperator(
    #     task_id='download_a',
    #     bash_command='sleep 10'
    # )
 
    # download_b = BashOperator(
    #     task_id='download_b',
    #     bash_command='sleep 10'
    # )
 
    # download_c = BashOperator(
    #     task_id='download_c',
    #     bash_command='sleep 10'
    # )
 
    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )
 

    ## We can group the transforms tasks into the "tansforms" task using TaskGoup instead of Subdags
    transforms = transform_tasks()

    # ## We can group the transform tasks into one "tranforms" task
    # transforms = SubDagOperator(
    #     task_id='transforms',
    #     subdag=subdag_transforms(dag.dag_id, 'transforms', args)
    # )

    # transform_a = BashOperator(
    #     task_id='transform_a',
    #     bash_command='sleep 10'
    # )
 
    # transform_b = BashOperator(
    #     task_id='transform_b',
    #     bash_command='sleep 10'
    # )
 
    # transform_c = BashOperator(
    #     task_id='transform_c',
    #     bash_command='sleep 10'
    # )
 
    ## Set up the dependencies
    # [download_a, download_b, download_c] >> check_files >> [transform_a, transform_b, transform_c]
    downloads >> check_files >> transforms