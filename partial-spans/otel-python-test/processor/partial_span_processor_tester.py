import os
import time

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
  OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs._internal.export import SimpleLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export.partial_span_processor import PartialSpanProcessor

# Create a TracerProvider
provider = TracerProvider()

# Configure OTLP exporters
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
logs_endpoint = os.getenv("OTEL_LOGS_ENDPOINT")
span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint,
                                 insecure=True)  # grpc
log_exporter = OTLPLogExporter(endpoint=logs_endpoint)  # http

# Use a PartialSpanProcessor for efficient exporting
span_processor = PartialSpanProcessor(span_exporter,
                                      SimpleLogRecordProcessor(log_exporter))
provider.add_span_processor(span_processor)

# Set the global TracerProvider
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Start a span (logs heartbeat and stop events)
with tracer.start_as_current_span("partial_span_1"):
  print("partial_span_1 is running")
  with tracer.start_as_current_span("partial_span_2"):
    print("partial_span_2 is running")
    with tracer.start_as_current_span("partial_span_3"):
      print("partial_span_3 is running")
      time.sleep(10)

provider.shutdown()
