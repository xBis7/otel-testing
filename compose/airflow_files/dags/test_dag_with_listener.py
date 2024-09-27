from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonVirtualenvOperator
from datetime import datetime
from airflow_provider_opentelemetry.hooks.otel import OtelHook
from opentelemetry import trace
import time

# Define default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
}

# Define the DAG (Directed Acyclic Graph)
with DAG(
    'test_dag_with_listener',
    default_args=args,
    schedule=None,  # Updated schedule_interval to schedule
    catchup=False,
) as dag:

    # Get otel hook
    otel_hook = OtelHook("otel_conn")

    # Span decorator for setup1_func
    @otel_hook.span
    def setup1_func():
        span = trace.get_current_span()
        span.set_attribute('app.msg', 'sleeping for 1 second')
        time.sleep(1)

    def setup2_func(**dag_context):
        with otel_hook.start_as_current_span(name="do_setup", dag_context=dag_context) as s:
            s.set_attribute("data quality", "fair")
            s.set_attribute("description", "You can add attributes in otel hook to have business or data specific details on top of existing task instance span.")
            print("Setup_2 -> hook_1")
            with otel_hook.start_as_current_span(name="do_sleep") as ss:
                ss.set_attribute("sleep for", "one second")
                time.sleep(1)
                print("Setup_2 -> hook_2")

    # Task functions
    def task_1_func():
        for i in range(5):
            time.sleep(3)
            print(f"Task_1, iteration '{i}'")
        print("Task_1 finished")

    def task_2_func():
        for i in range(3):
            time.sleep(2)
            print(f"Task_2, iteration '{i}'")
        print("Task_2 finished")

    def task_3_func():
        for i in range(7):
            time.sleep(3)
            print(f"Task_3, iteration '{i}'")
        print("Task_3 finished")

    def task_4_func(**dag_context):
        with otel_hook.start_as_current_span(name="build_lib", dag_context=dag_context) as s:
            s.set_attribute("component", "build_lib")

            with otel_hook.start_as_current_span(name="build_mod1") as s1:
              s1.set_attribute("component", "mod1")
              print("Building module 1")
              time.sleep(5)

            with otel_hook.start_as_current_span(name="build_mod2") as s2:
              s2.set_attribute("component", "mod2")
              print("Building module 2")
              time.sleep(7)

        with otel_hook.start_as_current_span(name="test_lib", dag_context=dag_context) as ss:
            ss.set_attribute("component", "test_lib")

            with otel_hook.start_as_current_span(name="test_mod1") as ss1:
              ss1.set_attribute("component", "mod1")
              print("Testing module 1")
              time.sleep(4)

            with otel_hook.start_as_current_span(name="test_mod2") as ss2:
              ss2.set_attribute("component", "mod2")
              print("Testing module 2")
              time.sleep(6)

    # Setup PythonOperator tasks
    t01 = PythonOperator(
        task_id="setup1",
        python_callable=setup1_func
    )

    t02 = PythonOperator(
        task_id="setup2",
        python_callable=setup2_func
    )

    # t1 = PythonOperator(
    #     task_id='task_1',
    #     python_callable=task_1_func,
    # )

    # t2 = PythonOperator(
    #     task_id='task_2',
    #     python_callable=task_2_func,
    # )

    # t3 = PythonOperator(
    #     task_id='task_3',
    #     python_callable=task_3_func,
    # )

    t4 = PythonOperator(
        task_id='task_4',
        python_callable=task_4_func,
    )

    t5 = PythonVirtualenvOperator(
      task_id='task_5',
      python_callable=task_4_func,
      requirements=['airflow-provider-opentelemetry==1.0.3'],
      system_site_packages=True,
    )

    # Define task dependencies
    # t01 >> t02 >> t1 >> t2 >> t3 >> t4
    t01 >> t02 >> t4 >> t5