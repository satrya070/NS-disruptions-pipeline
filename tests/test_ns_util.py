
import json
import datetime
import zoneinfo

from unittest.mock import patch
from ns_disruptions.ns_util import process_ns_data
from ns_disruptions.data_interfaces.ns_dataclasses import DisruptionData, DisruptionStationLink


@patch("ns_disruptions.ns_util.datetime")
def test_process_ns_data(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2025, 5, 28, 15, 7, 1, tzinfo=zoneinfo.ZoneInfo("Europe/Amsterdam"))

    with open("./tests/resources/ns_api_data.json") as f:
        ns_api_data = json.load(f)

    processed_data = process_ns_data(ns_api_data)
    processed_data_single_conseq = processed_data[0]
    processed_data_calamity = processed_data[1]

    expected_data_single_conseq = (
        DisruptionData(id='6056540', type='DISRUPTION', impact=3, fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam'))),
        [
            DisruptionStationLink(id='6056540', code='HNO', level='LESS_TRAINS', fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam'))), DisruptionStationLink(id='6056540', code='RAT', level='LESS_TRAINS', fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, 1, 327237, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam')))
        ]
    )

    expected_data_calamity = (
        DisruptionData(id='6ffa1726-cb80-44e7-ba7f-c6bc9d824d9c', type='CALAMITY', fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam'))),
        []
    )

    processed_data_calamity

    assert processed_data_single_conseq[0] == expected_data_single_conseq[0]
    assert processed_data_calamity == expected_data_calamity
    # TODO assert maintenance, multiconseq

    print(processed_data_calamity[0])
    assert False



if __name__ == "__main__":
    test_process_ns_data()