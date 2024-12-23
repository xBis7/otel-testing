from sdk_provider import get_sdk_instance, SdkProvider


def short_lived_spans(sdk_provider: SdkProvider):
    with sdk_provider.start_root_span(span_name="short_root_span") as root_span:

        root_carrier = sdk_provider.inject()
        parent_ctx = sdk_provider.extract(root_carrier)

        for counter in range(3):
            with sdk_provider.start_child_span(
                    span_name=f"short_sub_span{counter}",
                    parent_context=parent_ctx) as s:
                s.set_attribute("sub_span_num", counter)
                print(f"Very short lived task, sub-span-{counter}")

def unfinished_parent_span(sdk_provider: SdkProvider):
    span = sdk_provider.start_root_span(span_name="unfinished_root_span", start_as_current=False)
    print("===============")
    print(span.end_time)
    print("===============")
    sdk_provider.span_exporter.export((span,))
    root_carrier = sdk_provider.inject()
    parent_ctx = sdk_provider.extract(root_carrier)

    for counter in range(3):
        with sdk_provider.start_child_span(
                span_name=f"unfinished_sub_span{counter}",
                parent_context=parent_ctx) as s:
            s.set_attribute("sub_span_num", counter)
            print(f"Unfinished function, sub-span-{counter}")

    span.set_attribute("who", "x")
    sdk_provider.span_exporter.export((span,))
    sdk_provider.span_exporter.export((span,))
    sdk_provider.span_exporter.export((span,))

    span.end()
    print("===============")
    print(span)
    print("===============")

def long_lived_parent_span(sdk_provider: SdkProvider):
    pass
    # tracer = sdk_provider.get_tracer()
    #
    # with tracer.start_as_current_span(name="current_root_span") as root_span:
    #     with tracer.start_as_current_span(name="current_sub_span1") as sub_span:
    #         print("Current sub span 1")
    #     with tracer.start_as_current_span(name="current_sub_span2") as sub_span:
    #         print("Current sub span 2")

if __name__ == "__main__":
    sdk_provider = get_sdk_instance(use_simple_processor=True)
    short_lived_spans(sdk_provider)
    unfinished_parent_span(sdk_provider)
    long_lived_parent_span(sdk_provider)
