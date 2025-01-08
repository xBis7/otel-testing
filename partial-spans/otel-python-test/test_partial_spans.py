import time

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

def long_lived_spans(sdk_provider: SdkProvider):
    span = sdk_provider.start_root_span(span_name="long_lived_spans", start_as_current=False)

    root_carrier = sdk_provider.inject()
    parent_ctx = sdk_provider.extract(root_carrier)

    for counter in range(3):
        with sdk_provider.start_child_span(
                span_name=f"sub_span{counter}",
                parent_context=parent_ctx) as s:
            s.set_attribute("sub_span_num", counter)
            print(f"Unfinished function, sub-span-{counter}")
        time.sleep(20)

    span.set_attribute("who", "x")

    span.end()

if __name__ == "__main__":
    sdk_provider = get_sdk_instance(use_simple_processor=True)
    short_lived_spans(sdk_provider)
    long_lived_spans(sdk_provider)
