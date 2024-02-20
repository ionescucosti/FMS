## Fleet Management System (FMS)
### contains 3 microservices:
- fleet-management-service: APIs http://0.0.0.0:8000/docs
                            consumer that get events from queue='penalty_points' and update driver's points in db 
- gps_simulator_service: mockup to produce event for driver with id 1 and publish to queue = 'gps'
- vehicle_monitoring_system_service: check all events from queue = 'gps', apply penalty points and publish them 
  to queue='penalty_points'



### Run docker-compose.yml to build and run docker images for each service:
- cd /FMS
- docker-compose up --build






### In order to run project locally:

- cd /fleet_management_service:
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    CMD uvicorn main:app --host 0.0.0.0 --port 8000
    CMD python consumer.py
- 
- cd /gps_simulator_service:
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    CMD uvicorn gps_simulator_service:app
    

- cd /vehicle_monitoring_system_service
    RUN pip install --upgrade pip
    RUN pip install --no-cache-dir -r requirements.txt
    CMD uvicorn vehicle_monitoring_system_service:app

