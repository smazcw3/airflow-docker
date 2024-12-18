Introduction
------------
**Apache Airflow** is an open-source platform for authoring, scheduling and monitoring data and computing workflows. Airflow is the de-facto standard for defining ETL/ELT pipelines as Python code.

**Docker** is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime.

Installing Apache Airflow via Docker
------------------------------------
1. Create a folder, for e.g. `airflow-docker`. Within the folder, download the docker compose file from [here](https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml) and save it as `docker-compose.yaml`.

2. Create a `.env` file within folder and copy the following:

	~~~
	AIRFLOW_IMAGE_NAME=apache/airflow:2.4.2
	AIRFLOW_UID=50000
	~~~

2. Open the terminal and go that folder, and type `docker-compose up -d`.

    ![alt text](images/docker-airflow.png "Installing airflow through docker")

	There will be some additional folders that would be created as shown below:

	![alt text](images/docker-airflow2.png "Airflow through docker")


With this command, docker installs airflow within it. To check, open a web browser and go to `localhost:8080` and you will see something like below:
![alt text](images/airflow-login.png "Airflow login page")

3. Login through the airflow page using the following credentials:
	~~~
	Username : airflow
	Password : airflow
	~~~

4. Once you have logged in, the following page would be displayed
![alt text](images/airflow-login2.png "Airflow login page")
![alt text](images/airflow-login3.png "Airflow login page")


Important Notes
---------------
+ Docker Compose (`docker compose`) is used to run multiple containers as a single service. For example, suppose we had an application which required NGNIX and MySQL, we could create one file which would start both the containers as a service without the need to start each one separately.

+ We can run the docker-compose file using `docker compose -f {compose file name} up`

+ We can monitor tasks with Celery Flower. Celery Flower is a web-based monitoring tool for Celery, a distributed task queue for Python. It provides a visual interface for monitoring and managing Celery clusters, allowing users to view task progress, task history, and worker status in real-time.
In order to access Flower, we have to do `docker compose down && docker compose --profile flower up -d`. To check, open a web browser and go to `localhost:5555`

+ We can restart airflow instance through docker by `docker compose down && docker compose up -d`

+ Run the airlfow with elastic search instance by `docker compose -f docker-compose-es.yaml up -d`

+ To stop and restart airflow with elastic search instance, use `docker compose -f docker-compose-es.yaml stop && docker compose -f docker-compose-es.yaml up -d`

+ We can go inside the bash session of any container. For e.g. use `docker exec -it airflow-docker-airflow-scheduler-1 /bin/bash` where `airflow-docker-airflow-scheduler-1` is the container name.

+ Lists all running containers in docker engine using `docker ps`

+ Lists containers related to images declared in docker-compose file using `docker compose ps`

+ **Docker Vs Kubernets** -- Docker is a container technology that helps create an isolated environment for applications while Kubernetes is a container orchestration platform that manages the cluster of multiple containers.

+ **ElasticSearch** -- Elastic search is the search engine for our data. Basically, with elastic search, we are able to search, analyze and visualize our data.

Airflow has several parameters to tune your tasks and DAGs concurrency. Starting from the configuration settings
+ parallelism / AIRFLOW__CORE__PARALELISM
	- This defines the maximum number of task instances that can run in Airflow per scheduler. By default, you can execute up to 32 tasks at the same time. If you have 2 schedulers: 2 x 32 = 64 tasks.
	- What value to define here depends on the resources you have and the number of schedulers running.

+ max_active_tasks_per_dag / AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG
	- This defines the maximum number of task instances allowed to run concurrently in each DAG. By default, you can execute up to 16 tasks at the same time for a given DAG across all DAG Runs.

+ max_active_runs_per_dag / AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG
	- This defines the maximum number of active DAG runs per DAG. By default, you can have up to 16 DAG runs per DAG running at the same time.

+ Hook is an interface that encapsulates the complexity of interacting with an external system.


Operators
---------
Operators are the building blocks of Airflow DAGs. They contain the logic of how data is processed in a pipeline. Each task in a DAG is defined by instantiating an operator. An operator describes a single task of the workflow. 

Some of the common used operators are:
+ BashOperator 
+ PythonOperator 
+ EmailOperator
+ MySqlOperator
+ DockerOperator
+ KubernetesPodOperator
+ SnowflakeOperator


Trigger rules for task dependecies:
-----------------------------------
`all_success` - All the upstream tasks needs to be successful in order for the downstream tasks to be succeeded.

`all_failed` - If all the upstream tasks failed, then the downstream task is triggered. If one of the upstream task gets succeeded, then downstream task is skipped.

`all_done` - The downstream task gets triggered regardless of the success or skipping of the upstream tasks.

`one_success` - The downstream task gets triggered as soon as one of the immediate previous upstream tasks gets succeeded.

`one_failed` - The downstream task gets triggered as soon as the immediate previous upstream tasks gets skipped.

`none_failed` - The downstream task gets triggered as soon as the all the immediate previous upstream tasks gets succeeded or skipped.

`none_failed_min_one_success` - The downstream task gets triggered if one of the immediate previous upstream tasks gets succeeded and others have skipped.

References
----------
+ https://pythonspeed.com/articles/distributing-software/
+ https://www.kdnuggets.com/2023/07/docker-tutorial-data-scientists.html
+ https://docs.docker.com/guides/workshop/08_using_compose/
+ https://marclamberti.com/blog/variables-with-apache-airflow/
+ https://marclamberti.com/blog/how-to-use-dockeroperator-apache-airflow/
+ https://www.astronomer.io/docs/learn/what-is-an-operator
+ https://medium.com/nerd-for-tech/airflow-catchup-backfill-demystified-355def1b6f92 (Airflow catchup Vs Backfill)