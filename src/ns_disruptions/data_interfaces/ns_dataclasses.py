from dataclasses import dataclass

@dataclass
class DisruptionData:
    id: str = None
    type: str = None
    niveau: str = None
    coordinates: str = None
    impact: int
    fetch_timestamp: str


@dataclass
class DisruptionStationLink:
    id: str = None
    code: str = None
    level: str = None
    fetch_timestamp: str