

from datetime import datetime
from zoneinfo import ZoneInfo
from ns_disruptions.data_interfaces.ns_dataclasses import (
    DisruptionData, DisruptionStationLink
)


def process_ns_data(ns_api_data: list[dict]) -> list[tuple[DisruptionData, list[DisruptionStationLink]]]:
    """
    takes in raw ns api data and extract all relevant fields into data objects
    """
    processed_data = []
    for disruption_instance in ns_api_data:
        # data layout can differ between: DISRUPTION, CALAMITY, MAINTENANCE
        disruption_type = disruption_instance["type"]

        # TODO handle all types
        if disruption_type == "CALAMITY":
            continue

        fetch_timestamp = datetime.now(ZoneInfo("Europe/Amsterdam"))

        # for disruption_data in disruption_instance:
        disruption = DisruptionData(
            id=disruption_instance.get("id"),
            type=disruption_type,
            impact=disruption_instance.get("impact").get("value"),
            fetch_timestamp=fetch_timestamp,
        )

        disrupted_stations = []
        for publication in disruption_instance["publicationSections"]:
            level = publication["consequence"]["level"]
            consequence_stations = publication["consequence"]["section"]["stations"]

            for station in consequence_stations:
                disrupted_station = DisruptionStationLink(
                    id=disruption_instance.get("id"),
                    code=station.get("stationCode"),
                    level=level,
                    fetch_timestamp=fetch_timestamp
                )
                disrupted_stations.append(disrupted_station)

        processed_data.append((disruption, disrupted_stations))

    return processed_data


def process_publications(publications: dict) -> list[str]:
    """
    takes in a raw publications ns data and extracts the affected stations
    """
    for publication in publications:
        if publication["sectionType"] == "NL":
            consequence = publication["consequence"]
            consequence_stations = consequence["section"]["stations"]

            for station in consequence_stations:
                print(station["stationCode"])
                