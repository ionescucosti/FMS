# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /gps_app
WORKDIR /gps_app

# Copy the current directory contents into the container at /gps_app
COPY . /gps_app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME GPSSimulatorService

# Run gps_simulator.py when the container launches
CMD ["python", "gps_simulator_service.py", "--host", "0.0.0.0", "--port", "8001"]
