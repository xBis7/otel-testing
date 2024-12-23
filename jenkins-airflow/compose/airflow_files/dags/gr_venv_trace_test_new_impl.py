from airflow.decorators import dag, task
import pendulum

import logging
from pprint import pformat,pprint

@task(task_id="alpha")
def alpha_impl(**context):
    task_logger = logging.getLogger("airflow.task")

    task_logger.info("Starting alpha_impl")
    pprint(context)

@task.virtualenv(
    task_id="beta_venv",
    # op_kwargs={'context_carrier': '{{ ti.context_carrier }}'},
    requirements=["opentelemetry-instrumentation-requests"],
    system_site_packages=True,
    use_dill=True,
)
def beta_impl(context_carrier):
    import ast
    import requests
    import logging
    from airflow.traces import otel_tracer
    from airflow.traces.tracer import Trace
    from pprint import pformat,pprint

    # get the airflow.task logger
    task_logger = logging.getLogger("airflow.task")

    # get the Open Telemetry hook
    otel_airflow_tracer = otel_tracer.get_otel_tracer_for_task(Trace)

    task_logger.info("Starting beta_impl")

    # context_carrier is passed as a string. Convert it back to a dictionary.
    context_carrier = ast.literal_eval(context_carrier)

    ti_span_context = Trace.extract(context_carrier)

    otel_tracer_provider = otel_airflow_tracer.get_otel_tracer_provider()

    # If we want to hook up library instrumentation we have to connect the tracer provider like this
    # It needs the instrumentation library to be installed though. 
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    RequestsInstrumentor().instrument(tracer_provider=otel_tracer_provider)
    
    with otel_airflow_tracer.start_child_span(span_name="beta_impl", parent_context=ti_span_context) as s:
        task_logger.info("Starting beta_impl inner")

        # If we don't set the parent context, it will get it like so
        # trace.get_current_span().get_span_context()
        # and then start_as_current_span()
        with otel_airflow_tracer.start_child_span(span_name="get_version") as ss:
            response = requests.get("https://api.github.com/users/xBis7/repos")
            task_logger.info("Response: %s", response.json())
            
            ss.set_attribute("test.version_response", pformat(response.json()))

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["test"],
)
def gr_venv_trace_test_new_impl():
    alpha_task = alpha_impl()
    # beta_task = beta_impl()
    beta_task = beta_impl(context_carrier='{{ ti.context_carrier }}')

    alpha_task >> beta_task

gr_venv_trace_test_new_impl()
