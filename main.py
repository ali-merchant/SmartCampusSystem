from pprint import pprint

from cli import collect_request
from pipeline import process_raw_request


def main():
    raw = collect_request()
    response, router_output = process_raw_request(raw)

    if router_output:
        print("Router output:")
        pprint(router_output, width=80, sort_dicts=False)
    print("Final response:")
    pprint(response, width=80, sort_dicts=False)


if __name__ == "__main__":
    main()