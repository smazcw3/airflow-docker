from airflow import DAG, Dataset
from airflow.decorators import task

from datetime import datetime

#Define the datasets
my_file = Dataset("/tmp/my_file.txt")
my_file_2 = Dataset("/tmp/my_file_2.txt")

with DAG(
    dag_id="producer",
    schedule="@daily", #schedule is used since airflow 2.4+ instead of schedule_interval
    start_date=datetime(2024, 1, 1),
    catchup=False
):
    
    #outlets indicate that the given task will update the dataset <my_file>
    @task(outlets=[my_file])
    def update_dataset():
        with open(my_file.uri, "a+") as f:
            f.write("producer update")

    #outlets indicate that the given task will update the dataset <my_file>
    @task(outlets=[my_file_2])
    def update_dataset_2():
        with open(my_file_2.uri, "a+") as f:
            f.write("producer update")

    update_dataset() >> update_dataset_2()