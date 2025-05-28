
import json
import datetime
import zoneinfo

from unittest.mock import patch
from ns_disruptions.ns_util import process_ns_data
from ns_disruptions.data_interfaces.ns_dataclasses import DisruptionData, DisruptionStationLink


@patch("ns_disruptions.ns_util.datetime")
def test_process_ns_data(mock_datetime):
    mock_datetime.now.return_value = datetime.datetime(2025, 5, 28, 15, 7, 1, 327237, tzinfo=zoneinfo.ZoneInfo("Europe/Amsterdam"))

    with open("./tests/resources/ns_api_data.json") as f:
        ns_api_data = json.load(f)

    processed_data = process_ns_data(ns_api_data)
    processed_data_single_conseq = processed_data[0]

    expected_data_single_conseq = (
        DisruptionData(id='6056540', type='DISRUPTION', coordinates=None, impact=3, fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, 1, 327237, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam'))),
        [
            DisruptionStationLink(id='6056540', code='HNO', level='LESS_TRAINS', fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, 1, 327237, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam'))), DisruptionStationLink(id='6056540', code='RAT', level='LESS_TRAINS', fetch_timestamp=datetime.datetime(2025, 5, 28, 15, 7, 1, 327237, tzinfo=zoneinfo.ZoneInfo(key='Europe/Amsterdam')))
        ]
    )

    assert processed_data_single_conseq == expected_data_single_conseq
    # TODO assert maintenance, calamity, multiconseq


if __name__ == "__main__":
    test_process_ns_data()