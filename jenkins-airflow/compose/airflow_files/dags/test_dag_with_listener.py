from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.utils.types import DagRunTriggeredByType
from datetime import datetime
from opentelemetry import trace
import time

# Function to be run inside the virtual environment
def custom_task():
    return "VirtualEnv task completed"

# Function to pull data from XCom
def pull_xcom_data(ti):
    message = ti.xcom_pull(task_ids='run_with_virtualenv', key='custom_key')
    print(f"Pulled message from XCom: {message}")

# Define default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
}

# Define the DAG
with DAG(
    'test_dag_with_listener',
    default_args=args,
    # schedule=None,
    catchup=False,
) as dag:

    # Define the PythonVirtualenvOperator task
    run_with_virtualenv = PythonVirtualenvOperator(
        task_id='run_with_virtualenv',
        python_callable=custom_task,
        system_site_packages=True,
    )

    # Define a task to pull the XCom data
    pull_xcom = PythonOperator(
        task_id='pull_xcom_task',
        python_callable=pull_xcom_data,
    )

    run_with_virtualenv >> pull_xcom
