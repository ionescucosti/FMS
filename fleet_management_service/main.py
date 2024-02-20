from databases import Database
from database import database
from models import Vehicle, Driver, Trip
from schemas import vehicles, drivers, trips
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


# Dependency to get the database connection
async def get_database():
    return database


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# Vehicle CRUD
@app.get("/vehicles/{vehicle_id}", response_model=Vehicle)
async def read_vehicle(vehicle_id: int, db: Database = Depends(get_database)):
    query = vehicles.select().where(vehicles.c.id == vehicle_id)
    result = await db.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return result


@app.post("/vehicles/", response_model=Vehicle)
async def create_vehicle(vehicle: Vehicle, db: Database = Depends(get_database)):
    query = vehicles.insert().values(id=vehicle.id, type=vehicle.type, registration=vehicle.registration)
    try:
        await db.execute(query)
        return vehicle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating vehicle: {str(e)}")


@app.put("/vehicles/", response_model=Vehicle)
async def update_vehicle(updated_vehicle: Vehicle, db: Database = Depends(get_database)):
    query = vehicles.update().where(vehicles.c.id == Vehicle.id).values(
        type=updated_vehicle.type,
        registration=updated_vehicle.registration
    )
    try:
        await db.execute(query)
        return updated_vehicle
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating vehicle: {str(e)}")


@app.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Database = Depends(get_database)):
    query = vehicles.delete().where(vehicles.c.id == vehicle_id)
    try:
        await db.execute(query)
        return {"message": "Vehicle deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting vehicle: {str(e)}")


# Drivers CRUD
@app.get("/drivers/{driver_id}", response_model=Driver)
async def read_driver(driver_id: int, db: Database = Depends(get_database)):
    query = drivers.select().where(drivers.c.id == driver_id)
    result = await db.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    return result


@app.post("/drivers/", response_model=Driver)
async def create_driver(driver: Driver, db: Database = Depends(get_database)):
    query = drivers.insert().values(
        id=driver.id,
        fullName=driver.fullName,
        points=driver.points,
    )
    try:
        await db.execute(query)
        return driver
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating driver: {str(e)}")


@app.put("/drivers/", response_model=Driver)
async def update_driver(updated_driver: Driver, db: Database = Depends(get_database)):
    query = drivers.update().where(drivers.c.id == updated_driver.id).values(
        fullName=updated_driver.fullName,
        points=updated_driver.points
    )
    try:
        await db.execute(query)
        return updated_driver
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating driver: {str(e)}")


@app.delete("/drivers/{driver_id}")
async def delete_driver(driver_id: int, db: Database = Depends(get_database)):
    query = drivers.delete().where(drivers.c.id == driver_id)
    try:
        await db.execute(query)
        return {"message": "Driver deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting driver: {str(e)}")


# Trips CRUD
@app.get("/trips/{trip_id}", response_model=Trip)
async def read_trip(trip_id: int, db: Database = Depends(get_database)):
    query = trips.select().where(trips.c.id == trip_id)
    result = await db.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return result


@app.post("/trips/", response_model=Trip)
async def create_trip(trip: Trip, db: Database = Depends(get_database)):
    query = trips.insert().values(
        id=trip.id,
        departureGeoPoint=trip.departureGeoPoint,
        destinationGeoPoint=trip.destinationGeoPoint,
    )
    try:
        await db.execute(query)
        return trip
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating trip: {str(e)}")


@app.put("/trips/", response_model=Trip)
async def update_trip(updated_trip: Trip, db: Database = Depends(get_database)):
    query = trips.update().where(trips.c.id == Trip.id).values(
        departureGeoPoint=updated_trip.fullName,
        destinationGeoPoint=updated_trip.points
    )
    try:
        await db.execute(query)
        return updated_trip
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating trip: {str(e)}")


@app.delete("/trips/{trip_id}")
async def delete_trip(trip_id: int, db: Database = Depends(get_database)):
    query = trips.delete().where(trips.c.id == trip_id)
    try:
        await db.execute(query)
        return {"message": "Trip deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting trip: {str(e)}")


# Assigning endpoints
@app.post("/vehicles/{vehicle_id}/assign-driver/{driver_id}")
async def assign_driver_to_vehicle(vehicle_id: int, driver_id: int, db: Database = Depends(get_database)):
    query = vehicles.select().where(vehicles.c.id == vehicle_id)
    vehicle = await db.fetch_one(query)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    query = drivers.select().where(drivers.c.id == driver_id)
    driver = await db.fetch_one(query)
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    query = vehicles.update().where(vehicles.c.id == vehicle_id).values(driver_id=driver_id)
    try:
        await db.execute(query)
        return {"message": "Driver assigned to Vehicle successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error assigning driver to vehicle: {str(e)}")


@app.post("/trips/{trip_id}/assign-vehicle/{vehicle_id}")
async def assign_vehicle_to_trip(trip_id: int, vehicle_id: int, db: Database = Depends(get_database)):
    query = trips.select().where(trips.c.id == trip_id)
    trip = await db.fetch_one(query)
    if trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")

    query = vehicles.select().where(vehicles.c.id == vehicle_id)
    vehicle = await db.fetch_one(query)
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    query = trips.update().where(trips.c.id == trip_id).values(vehicle_id=vehicle_id)
    try:
        await db.execute(query)
        return {"message": "Vehicle assigned to Trip successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error assigning vehicle to trip: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
