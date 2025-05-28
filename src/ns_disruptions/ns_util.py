import datetime

from zoneinfo import ZoneInfo
from ns_disruptions.data_interfaces.ns_dataclasses import (
    DisruptionData, DisruptionStationLink
)


def process_ns_data(ns_api_data: dict) -> tuple[DisruptionData, list[DisruptionStationLink]]:
    """
    takes in raw ns api data and extract all relevant fields into data objects
    """
    # data layout can differ between: DISRUPTION, CALAMITY, MAINTENANCE
    # TODO handle all types
    disruption_type = ns_api_data["type"]
    fetch_timestamp = now_nl = datetime.now(ZoneInfo("Europe/Amsterdam"))

    for disruption_data in ns_api_data:
        disruption = DisruptionData(
            id=disruption_data.get("id"),
            type=disruption_data.get("type"),
            impact=disruption_data.get("impact").get("value"),
            fetch_timestamp=fetch_timestamp,
        )

        disrupted_stations = []
        for publication in disruption_data["publicationSections"]:
            level = publication["consequence"]["level"]
            consequence_stations = publication["consequence"]["section"]["stations"]

            for station in consequence_stations:
                disrupted_station = DisruptionStationLink(
                    id=disruption_data.get("id"),
                    code=station.get("stationCode"),
                    level=level,
                    fetch_timestamp=fetch_timestamp
                )
                disrupted_stations.append(disrupted_station)

    return tuple(disruption, disrupted_stations)


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
                