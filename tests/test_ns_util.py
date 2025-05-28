
import json
from ns_disruptions.ns_util import process_ns_data


def test_process_ns_data():
    with open("./tests/resources/ns_api_data.json") as f:
        ns_api_data = json.load(f)

    processed_data = process_ns_data(ns_api_data)
    print(processed_data[0])

    assert False


if __name__ == "__main__":
    test_process_ns_data()