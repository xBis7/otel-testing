from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import time

# Define default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
}

# Define the DAG (Directed Acyclic Graph)
with DAG(
    'test_dag_without_otel_code',
    default_args=args,
    schedule=None,  # Set to None for manual triggering
    catchup=False,  # Don't run previous DAG runs if they haven't been run before
) as dag:

    # Define a simple Python function for task 1
    def task_1_func():
      for i in range(5):
          time.sleep(3)
          print("Task_1, iteration '", i, "'")
      print("Task_1 finished")

    # Define another simple Python function for task 2
    def task_2_func():
        for i in range(3):
            time.sleep(2)
            print("Task_2, iteration '", i, "'")
        print("Task_2 finished")

    # Define the final Python function for task 3
    def task_3_func():
      for i in range(7):
          time.sleep(3)
          print("Task_3, iteration '", i, "'")
      print("Task_3 finished")

    # Create PythonOperator tasks
    t1 = PythonOperator(
        task_id='task_1',
        python_callable=task_1_func,
    )

    t2 = PythonOperator(
        task_id='task_2',
        python_callable=task_2_func,
    )

    t3 = PythonOperator(
        task_id='task_3',
        python_callable=task_3_func,
    )

    # Define task dependencies
    # task_1 -> task_2 -> task_3
    t1 >> t2 >> t3
