from datetime import date

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)

class TransportCollectionCreate(BaseModel):

    vehicle_number: str = Field(min_length=5,max_length=20)
    collection_date: date
    driver_name: str = Field(min_length=2,max_length=100)
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: float = Field( ge=0)
    evening_collection: float = Field(ge=0)
    fuel_expense: float = Field( ge=0)
    other_expense: float = Field(ge=0 )


    @field_validator("vehicle_number")
    @classmethod
    def validate_vehicle_number(cls, value):
        value = value.strip().upper()
        if not value:
            raise ValueError ("Vehicle number cannot be empty.")
        if " " in value:
            raise ValueError("Vehicle number cannot contain spaces.")
        return value


    @field_validator("driver_name")
    @classmethod
    def validate_driver_name(cls, value):
        value = value.strip()
        if any(char.isdigit() for char in value):
            raise ValueError("Driver name cannot contain numbers")
        return value

    @model_validator(mode="after")
    def validate_collection(self):
        total_collection = (
            self.morning_collection
            + self.evening_collection
        )

        total_expense = (
            self.fuel_expense
            + self.other_expense
        )
        if total_expense > total_collection:
            raise ValueError("Total expense cannot be greater than total collection"  )
        return self




class TransportCollectionUpdate(BaseModel):

    vehicle_number: str = Field(min_length=5,max_length=20)
    collection_date: date
    driver_name: str = Field(min_length=2,max_length=100)
    morning_trips: int = Field(ge=0)
    evening_trips: int = Field(ge=0)
    morning_collection: float = Field( ge=0)
    evening_collection: float = Field(ge=0)
    fuel_expense: float = Field( ge=0)
    other_expense: float = Field(ge=0 )


    @field_validator("vehicle_number")
    @classmethod
    def validate_vehicle_number(cls, value):
        value = value.strip().upper()
        if not value:
            raise ValueError ("Vehicle number cannot be empty.")
        if " " in value:
            raise ValueError("Vehicle number cannot contain spaces.")
        return value


    @field_validator("driver_name")
    @classmethod
    def validate_driver_name(cls, value):
        value = value.strip()
        if any(char.isdigit() for char in value):
            raise ValueError("Driver name cannot contain numbers")
        return value

    @model_validator(mode="after")
    def validate_collection(self):
        total_collection = (
            self.morning_collection
            + self.evening_collection
        )

        total_expense = (
            self.fuel_expense
            + self.other_expense
        )
        if total_expense > total_collection:
            raise ValueError("Total expense cannot be greater than total collection"  )
        return self


class TransportCollectionPatch(BaseModel):
    vehicle_number: str | None = Field(
        default=None,
        min_length=5,
        max_length=20
    )
    collection_date: date | None = None
    driver_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    morning_trips: int | None = Field(default=None, ge=0)
    evening_trips: int | None = Field(default=None, ge=0)
    morning_collection: float | None = Field(default=None, ge=0)
    evening_collection: float | None = Field(default=None, ge=0)
    fuel_expense: float | None = Field(default=None, ge=0)
    other_expense: float | None = Field(default=None, ge=0)

    @field_validator("vehicle_number")
    @classmethod
    def validate_vehicle_number(cls, value):
        if value is not None:
            value = value.strip().upper()

            if not value:
                raise ValueError("Vehicle number cannot be empty")

            if " " in value:
                raise ValueError("Vehicle number cannot contain spaces")

            return value

        return value

    @field_validator("driver_name")
    @classmethod
    def validate_driver_name(cls, value):
        if value is not None:
            value = value.strip()

            if any(char.isdigit() for char in value):
                raise ValueError("Driver name cannot contain numbers")

            return value

        return value


class TransportCollectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id : int
    vehicle_number : str
    collection_date : date
    driver_name : str
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


