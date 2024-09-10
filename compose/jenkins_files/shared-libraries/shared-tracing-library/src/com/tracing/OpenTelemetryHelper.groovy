package com.tracing

import io.opentelemetry.api.GlobalOpenTelemetry
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.SpanKind
import io.opentelemetry.context.Context
import io.opentelemetry.context.Scope

class OpenTelemetryHelper {

  // Initialize the OpenTelemetry Tracer
  def static tracer = GlobalOpenTelemetry.getTracer('shared-tracing-library')

  // Start a custom span
  static Span startSpan(String spanName) {
    return tracer.spanBuilder(spanName)
                     .setSpanKind(SpanKind.INTERNAL)
                     .startSpan()
  }

  // End a span
  static void endSpan(Span span) {
    if (span != null) {
      span.end()
    }
  }

  // Set attributes for a span
  static void setSpanAttribute(Span span, String key, String value) {
    if (span != null) {
      span.setAttribute(key, value)
    }
  }

  // Record exception in a span
  static void recordException(Span span, Exception e) {
    if (span != null) {
      span.recordException(e)
      span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR)
    }
  }

}
