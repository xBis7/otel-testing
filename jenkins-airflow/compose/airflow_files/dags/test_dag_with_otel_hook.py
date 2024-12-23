from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.python import PythonVirtualenvOperator
from airflow.traces import otel_tracer
from airflow.traces.tracer import Trace
from datetime import datetime, timezone
from airflow_provider_opentelemetry.hooks.otel import OtelHook
from airflow_provider_opentelemetry.util import (
    gen_span_id,
    gen_trace_id,
)
from opentelemetry import trace
from opentelemetry.propagate import inject, extract
from opentelemetry.propagators.textmap import Getter
from opentelemetry.context.context import Context
# from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
import time
import pydevd_pycharm

args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 0,
}

# Define the DAG (Directed Acyclic Graph)
with DAG(
    'test_dag_with_otel_hook',
    default_args=args,
    schedule=None,
    catchup=False,
) as dag:

    airflow_otel_tracer = otel_tracer.get_otel_tracer(Trace)
    print(f"type: {type(airflow_otel_tracer)}")

    # Get otel hook
    otel_hook = OtelHook("otel_conn")

    # pydevd_pycharm.settrace('host.docker.internal', port=3003, stdoutToServer=True, stderrToServer=True)

    # tracer = trace.get_tracer("trace_test.tracer",tracer_provider=otel_hook.tracer_provider)
    tracer = airflow_otel_tracer.get_tracer("trace_test.tracer")

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
    def task_1_func(**dag_context):
      start_time = time.time()
      # execution_datetime = datetime(2024, 10, 7, 17, 55, 57, 302285, tzinfo=timezone.utc)

      print(f"dag_context: {dag_context}")

      # print(f"xbis: __carrier: {airflow_otel_tracer.carrier}")

      current_context0 = trace.get_current_span().get_span_context()
      airflow_current_context0 = airflow_otel_tracer.get_current_span().get_span_context()

      dag_run = dag_context["dag_run"]
      ti = dag_context["ti"]
      task_instance = dag_context["task_instance"]
      carrier_from_context = dag_context["carrier"]
      print(f"xbis: carrier_from_context: {carrier_from_context} | ti.carrier: {ti.carrier} | task_instance.carrier: {task_instance.carrier}")
      
      context = airflow_otel_tracer.extract(ti.carrier)

      print(f"xbis: context: {context}")
      
      t_id = gen_trace_id(dag_run)
      s_id = gen_span_id(ti)
      print(f"t_id: {t_id} | s_id: {s_id}")
      print(f"curr_t_id: {current_context0.trace_id} | curr_s_id: {current_context0.span_id}")
      print(f"airf_curhr_t_id: {airflow_current_context0.trace_id} | airf_curr_s_id: {airflow_current_context0.span_id}")

      # pydevd_pycharm.settrace('host.docker.internal', port=3003, stdoutToServer=True, stderrToServer=True)
      # print("Waiting for debugger attach...")

      # Start a span and print the context before injecting
      # with airflow_otel_tracer.start_span_from_taskinstance(ti=task_instance, span_name="task_1_child_span", child = True) as s1:
          # print("Task_1, first part")

          # Start a new span using the extracted context
          # with airflow_otel_tracer.start_span("extracted_span") as span2:
          #     for i in range(5):
          #         # time.sleep(3)
          #         print(f"Task_1, iteration '{i}' with context propagation")
          #     print("Task_1 finished")

      end_time = time.time()
    
      # Calculate the time difference and format it to 2 decimal places
      elapsed_time = end_time - start_time
      print(f"Time taken: {elapsed_time:.2f} seconds")
      
      # end_datetime = datetime(2024, 10, 7, 17, 55, 59, 453854, tzinfo=timezone.utc)

      # 1. Calculate the duration in seconds (as a floating-point number)
      # duration = (end_datetime - execution_datetime).total_seconds()
      # formatted_duration = round(duration, 6)  # Round to 6 decimal places to match the format

      # # 2. Format the dates in ISO 8601 with timezone information
      # formatted_execution_date = execution_datetime.isoformat()
      # formatted_end_date = end_datetime.isoformat()

      # # 3. Print the formatted values
      # print(f"Duration: {formatted_duration}")  # Example output: 2.151569
      # print(f"End Date: {formatted_end_date}")  # Example output: 2024-10-07T17:55:59.453854+00:00
      # print(f"Execution Date: {formatted_execution_date}")  # Example output: 2024-10-07T17:55:57.302285+00:00

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
        ti = dag_context["ti"]
        task_instance = dag_context["task_instance"]
        carrier_from_context = dag_context["carrier"]
        print(f"xbis: carrier_from_context: {carrier_from_context} | ti.carrier: {ti.carrier} | task_instance.carrier: {task_instance.carrier}")
        
        with otel_hook.start_as_current_span(name="build_lib", dag_context=dag_context) as s:
            s.set_attribute("component", "build_lib")

            with otel_hook.start_as_current_span(name="build_mod1") as s1:
              s1.set_attribute("component", "mod1")
              print("Building module 1")
              # time.sleep(5)

            with otel_hook.start_as_current_span(name="build_mod2") as s2:
              s2.set_attribute("component", "mod2")
              print("Building module 2")
              # time.sleep(7)

        with otel_hook.start_as_current_span(name="test_lib", dag_context=dag_context) as ss:
            ss.set_attribute("component", "test_lib")

            with otel_hook.start_as_current_span(name="test_mod1") as ss1:
              ss1.set_attribute("component", "mod1")
              print("Testing module 1")
              # time.sleep(4)

            with otel_hook.start_as_current_span(name="test_mod2") as ss2:
              ss2.set_attribute("component", "mod2")
              print("Testing module 2")
              # time.sleep(6)

    # Setup PythonOperator tasks
    # t01 = PythonOperator(
    #     task_id="setup1",
    #     python_callable=setup1_func
    # )

    # t02 = PythonOperator(
    #     task_id="setup2",
    #     python_callable=setup2_func
    # )

    t1 = PythonOperator(
        task_id='task_1',
        python_callable=task_1_func,
    )

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

    # t5 = PythonVirtualenvOperator(
    #   task_id='task_5',
    #   python_callable=task_4_func,
    #   requirements=['airflow-provider-opentelemetry==1.0.3'],
    #   system_site_packages=True,
    # )

    # Define task dependencies
    # t01 >> t02 >> t1 >> t2 >> t3 >> t4
    t1 >> t4