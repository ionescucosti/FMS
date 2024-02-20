# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /monitoring_app
WORKDIR /monitoring_app

# Copy the current directory contents into the container at /monitoring_app
COPY . /monitoring_app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME FleetManagementService

# Run app.py when the container launches
CMD ["python", "vehicle_monitoring_system_service.py", "--host", "0.0.0.0", "--port", "8002"]
