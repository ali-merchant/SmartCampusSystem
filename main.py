from pprint import pprint

from cli import collect_request
from pipeline import process_raw_request


def main():
    # Run the CLI flow and process the request through the pipeline.
    # Handle user cancellation to avoid a hard crash.
    try:
        raw = collect_request()
        response, router_output = process_raw_request(raw)
    except (KeyboardInterrupt, EOFError):
        print("\nInput cancelled by user.")
        print()
        return
    except Exception as exc:
        print(f"\nUnexpected error: {exc}")
        print()
        return

    if router_output:
        print("Router output:")
        pprint(router_output, width=80, sort_dicts=False)
        print()
    print("Final response:")
    pprint(response, width=80, sort_dicts=False)
    print()


if __name__ == "__main__":
    main()