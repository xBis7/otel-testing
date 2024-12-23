// A simple wrapper for starting and ending spans from the shared library

def startSpan(String spanName) {
  def span = com.tracing.OpenTelemetryHelper.startSpan(spanName)
  return span
}

def endSpan(def span) {
  com.tracing.OpenTelemetryHelper.endSpan(span)
}

def setSpanAttribute(def span, String key, String value) {
  com.tracing.OpenTelemetryHelper.setSpanAttribute(span, key, value)
}

def recordException(def span, Exception e) {
  com.tracing.OpenTelemetryHelper.recordException(span, e)
}
