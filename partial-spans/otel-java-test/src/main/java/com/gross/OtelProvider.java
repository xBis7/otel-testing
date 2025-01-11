package com.gross;

import io.opentelemetry.api.OpenTelemetry;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.Scope;
import io.opentelemetry.context.propagation.TextMapGetter;
import io.opentelemetry.context.propagation.TextMapSetter;
import io.opentelemetry.exporter.logging.internal.ConsoleSpanExporterProvider;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.autoconfigure.spi.internal.DefaultConfigProperties;
import io.opentelemetry.sdk.trace.ReadWriteSpan;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.trace.export.SpanExporter;

import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

public class OtelProvider {

  private static final TextMapSetter<Map<String, String>> setter = Map::put;
  private static final TextMapGetter<Map<String, String>> getter =
      new TextMapGetter<Map<String, String>>() {
        @Override
        public Iterable<String> keys(Map<String, String> carrier) {
          return carrier.keySet();
        }

        @Override
        public String get(Map<String, String> carrier, String key) {
          return carrier.get(key);
        }
      };

  private final W3CTraceContextPropagator contextPropagator = W3CTraceContextPropagator.getInstance();

  public OtelProvider() {
    ConsoleSpanExporterProvider exporterProvider = new ConsoleSpanExporterProvider();
    DefaultConfigProperties configProperties = DefaultConfigProperties.create(Collections.emptyMap());
    SpanExporter exporter = exporterProvider.createExporter(configProperties);

    // 1. Create a SdkTracerProvider and configure it with a BatchSpanProcessor that uses a ConsoleSpanExporter
    SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                                           .addSpanProcessor(
                                               BatchSpanProcessor.builder(exporter)
                                                   // This will make sure that the span is exported fast.
                                                   .setScheduleDelay(java.time.Duration.ofMillis(500))
                                                   .build()
                                           )
                                           .build();

    // 2. Build an OpenTelemetry instance from the configured SdkTracerProvider
    OpenTelemetry openTelemetry = OpenTelemetrySdk.builder()
                                      .setTracerProvider(tracerProvider)
                                      .buildAndRegisterGlobal();

    // 3. Retrieve the tracer
    Tracer tracer = openTelemetry.getTracer("com.example.opentelemetry", "1.0.0");

    createTestSpans(tracer);

    // The span will be exported in 500 millis. 1000 millis is enough to get it on the output.
    try {
      Thread.sleep(1000);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
  }

  public void createTestSpans(Tracer tracer) {
    // Root span.
    Span rootSpan = tracer.spanBuilder("root-span").startSpan();

    Map<String, String> rootCarrier = new HashMap<>();

    try (Scope ignored = rootSpan.makeCurrent()) {
      // Since the root Span was made the current span, we can access its context.
      contextPropagator.inject(Context.current(), rootCarrier, setter);

      Context rootContext = contextPropagator.extract(Context.current(), rootCarrier, getter);

      for (int i = 0; i < 3; i++) {
        Span childSpan =
            tracer.spanBuilder("sub-span-" + i)
                .setParent(rootContext)
                .startSpan();

        System.out.println("Iteration '" + i + "'.");
        childSpan.end();

//        try {
//          Thread.sleep(10000);
//        } catch (InterruptedException e) {
//          throw new RuntimeException(e);
//        }
      }
    } finally {
      rootSpan.end();
    }
  }
}
