from dataclasses import dataclass
from datetime import date


@dataclass
class TransportCollectionModel:
    id: int
    vehicle_number: str
    collection_date: date
    driver_name: str
    morning_trips: int
    evening_trips: int
    morning_collection: float
    evening_collection: float
    fuel_expense: float
    other_expense: float
    total_trips: int
    total_collection: float
    total_expense: float
    net_collection: float

