from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

import time

# Initialize OpenTelemetry
resource = Resource(attributes={SERVICE_NAME: "airflow"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Configure OpenTelemetry to send traces to the OTLP Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# Define default arguments for the DAG
args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 1),
    'retries': 1,
}

# Define the DAG (Directed Acyclic Graph)
with DAG(
    'test_dag',
    default_args=args,
    schedule=None,  # Set to None for manual triggering
    catchup=False,  # Don't run previous DAG runs if they haven't been run before
) as dag:

    # Define a simple Python function for task 1
    def task_1_func():
        with tracer.start_as_current_span("task_1"):
            for i in range(5):
                time.sleep(3)
                print("Task_1, iteration '", i, "'")
            print("Task_1 finished")

    # Define another simple Python function for task 2
    def task_2_func():
        with tracer.start_as_current_span("task_2"):
            for i in range(3):
                time.sleep(2)
                print("Task_2, iteration '", i, "'")
            print("Task_2 finished")

    # Define the final Python function for task 3
    def task_3_func():
        with tracer.start_as_current_span("task_3"):
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
