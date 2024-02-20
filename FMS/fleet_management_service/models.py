from pydantic import BaseModel


class Vehicle(BaseModel):
    id: int
    type: str
    registration: str


class Driver(BaseModel):
    id: int
    fullName: str
    points: int


class Trip(BaseModel):
    id: int
    departureGeoPoint: str
    destinationGeoPoint: str