from airflow.decorators import dag, task
from airflow_provider_opentelemetry.hooks.otel import OtelHook
from opentelemetry import trace
import pendulum

import logging
from pprint import pformat,pprint

# get the airflow.task logger
task_logger = logging.getLogger("airflow.task")

# get the Open Telemetry hook
otel_hook = OtelHook("otel_default")

@task(task_id="alpha")
def alpha_impl(**context):
    task_logger.info("Starting alpha_impl")
    pprint(context)

@task(task_id="beta")
def beta_impl(**context):
    import requests

    task_logger.info("Starting beta_impl")
    pprint(context)

    # If we want to hook up library instrumentation we have to connect the tracer provider like this
    # It needs the instrumentation library to be installed though. 
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    RequestsInstrumentor().instrument(tracer_provider=otel_hook.tracer_provider)
        
    # We must use `otel_hook` here to ensure the span is created in the correct context
    with otel_hook.start_as_current_span(name="beta_impl", dag_context=context) as s:
        task_logger.info("Starting beta_impl inner")
        
        # Now we can use the standard trace API, but we have to hook up the tracer provider
        tracer = trace.get_tracer("trace_test.tracer",tracer_provider=otel_hook.tracer_provider)
        
        with tracer.start_as_current_span(name="get_version") as ss:
        # with otel_hook.start_as_current_span(name="get_version") as ss:
            response = requests.get("https://api.github.com/users/xBis7/repos")
            task_logger.info("Response: %s", response.json())
            
            ss.set_attribute("test.version_response", pformat(response.json()))

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
)
def gr_working_trace_test():
    alpha_task = alpha_impl()
    beta_task = beta_impl()

    alpha_task >> beta_task

gr_working_trace_test()