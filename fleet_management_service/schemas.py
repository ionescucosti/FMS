from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database import metadata

vehicles = Table(
    "vehicles",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("type", String),
    Column("registration", String, unique=True),
    Column("driver_id", ForeignKey("drivers.id")),
)

drivers = Table(
    "drivers",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("fullName", String),
    Column("points", Integer),
)

trips = Table(
    "trips",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("departureGeoPoint", String),
    Column("destinationGeoPoint", String),
    Column("vehicle_id", ForeignKey("vehicles.id")),
)