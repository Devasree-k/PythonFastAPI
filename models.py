from datetime import date
from pydantic import BaseModel, Field

class TransportCollectionCreate(BaseModel):

    vehicle_number: str = Field(min_length=8, max_length=15)
    collection_date: date
    driver_name: str = Field(min_length=2, max_length=100)
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: float = Field(ge=0)
    evening_collection: float = Field(ge=0)
    fuel_expense: float = Field(ge=0)
    other_expense: float = Field(ge=0)


class TransportCollectionUpdate(BaseModel):

    vehicle_number: str = Field(min_length=8, max_length=15)
    collection_date: date
    driver_name: str = Field(min_length=2, max_length=100)
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: float = Field(ge=0)
    evening_collection: float = Field(ge=0)
    fuel_expense: float = Field(ge=0)
    other_expense: float = Field(ge=0)

    