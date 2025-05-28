from dataclasses import dataclass

@dataclass
class DisruptionData:
    id: str = None
    type: str = None
    coordinates: str = None
    impact: int = -1
    fetch_timestamp: str = None


@dataclass
class DisruptionStationLink:
    id: str = None
    code: str = None
    level: str = None
    fetch_timestamp: str = None