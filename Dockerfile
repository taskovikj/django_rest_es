# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/
