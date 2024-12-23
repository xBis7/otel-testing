from datetime import datetime, timezone
import os
import socket

from opentelemetry import trace
from opentelemetry.context import Context, attach
from opentelemetry.trace import SpanContext, INVALID_TRACE_ID, INVALID_SPAN_ID, NonRecordingSpan, TraceFlags, Link
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

from dates import datetime_to_nano
from dotenv import load_dotenv
from opentelemetry.sdk.trace import TracerProvider, SpanProcessor, Tracer
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, HOST_NAME
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, ConsoleSpanExporter

class SdkProvider:

    def __init__(self, otlp_endpoint: str, is_debug: bool, use_simple_processor: bool) -> None:
        self.span_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        self.is_debug = is_debug
        self.use_simple_processor = use_simple_processor
        if use_simple_processor:
            self.span_processor: SpanProcessor = SimpleSpanProcessor(self.span_exporter)
        else:
            self.span_processor = BatchSpanProcessor(self.span_exporter)

        self.resource = Resource.create(
            attributes={HOST_NAME: socket.gethostname(), SERVICE_NAME: "tester"}
        )

    def get_otel_tracer_provider(self) -> TracerProvider:
        tracer_provider = TracerProvider(resource=self.resource)

        if self.is_debug:
            if self.use_simple_processor:
                span_processor_for_tracer_prov: SpanProcessor = SimpleSpanProcessor(ConsoleSpanExporter())
            else:
                span_processor_for_tracer_prov = BatchSpanProcessor(ConsoleSpanExporter())
        else:
            span_processor_for_tracer_prov = self.span_processor

        tracer_provider.add_span_processor(span_processor_for_tracer_prov)
        return tracer_provider

    def get_tracer(self, component: str | None = None) -> Tracer:
        tracer_provider = self.get_otel_tracer_provider()

        if component is None:
            component = __name__

        tracer = tracer_provider.get_tracer(component)

        return tracer

    def start_root_span(
        self,
        span_name: str,
        component: str | None = None,
        links=None,
        start_time=None,
        start_as_current: bool = True,
    ):
        """Start a root span."""
        # If no context is passed to the new span,
        # then it will try to get the context of the current active span.
        # Due to that, the context parameter can't be empty.
        # It needs an invalid context in order to declare the new span as root.
        invalid_span_ctx = SpanContext(
            trace_id=INVALID_TRACE_ID, span_id=INVALID_SPAN_ID, is_remote=True, trace_flags=TraceFlags(0x01)
        )
        invalid_ctx = trace.set_span_in_context(NonRecordingSpan(invalid_span_ctx))

        if links is None:
            _links = []
        else:
            _links = links

        return self._new_span(
            span_name=span_name,
            parent_context=invalid_ctx,
            component=component,
            links=_links,
            start_time=start_time,
            start_as_current=start_as_current,
        )

    def start_child_span(
        self,
        span_name: str,
        parent_context: Context | None = None,
        component: str | None = None,
        links=None,
        start_time=None,
        start_as_current: bool = True,
    ):
        """Start a child span."""
        if parent_context is None:
            # If no context is passed, then use the current.
            parent_span_context = trace.get_current_span().get_span_context()
            parent_context = trace.set_span_in_context(NonRecordingSpan(parent_span_context))
        else:
            context_val = next(iter(parent_context.values()))
            parent_span_context = None
            if isinstance(context_val, NonRecordingSpan):
                parent_span_context = context_val.get_span_context()

        if links is None:
            _links = []
        else:
            _links = links

        if parent_span_context is not None:
            _links.append(
                Link(
                    context=parent_span_context,
                    attributes={"meta.annotation_type": "link", "from": "parenttrace"},
                )
            )

        return self._new_span(
            span_name=span_name,
            parent_context=parent_context,
            component=component,
            links=_links,
            start_time=start_time,
            start_as_current=start_as_current,
        )

    def _new_span(
        self,
        span_name: str,
        parent_context: Context | None = None,
        component: str | None = None,
        links=None,
        start_time=None,
        start_as_current: bool = True,
    ):
        tracer = self.get_tracer(component=component)

        if start_time is None:
            start_time = datetime.now(tz=timezone.utc)

        if links is None:
            links = []

        if start_as_current:
            span = tracer.start_as_current_span(
                name=span_name,
                context=parent_context,
                links=links,
                start_time=datetime_to_nano(start_time),
            )
        else:
            span = tracer.start_span(
                name=span_name,
                context=parent_context,
                links=links,
                start_time=datetime_to_nano(start_time),
            )
            current_span_ctx = trace.set_span_in_context(NonRecordingSpan(span.get_span_context()))
            # We have to manually make the span context as the active context.
            # If the span needs to be injected into the carrier, then this is needed to make sure
            # that the injected context will point to the span context that was just created.
            attach(current_span_ctx)
        return span

    def inject(self) -> dict:
        """Inject the current span context into a carrier and return it."""
        carrier: dict[str, str] = {}
        TraceContextTextMapPropagator().inject(carrier)
        return carrier

    def extract(self, carrier: dict) -> Context:
        """Extract the span context from a provided carrier."""
        return TraceContextTextMapPropagator().extract(carrier)


def get_sdk_instance(use_simple_processor: bool = False) -> SdkProvider:
    # Load environment variables from .env file
    load_dotenv()

    # Retrieve the OTEL endpoint from environment
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not otlp_endpoint:
        raise ValueError("OTEL_EXPORTER_OTLP_ENDPOINT is not set in the '.env' file.")

    is_debug_str = os.getenv("debug_on")
    is_debug = is_debug_str.lower() == "true"

    return SdkProvider(
        otlp_endpoint=otlp_endpoint,
        is_debug=is_debug,
        use_simple_processor=use_simple_processor,
    )

    
