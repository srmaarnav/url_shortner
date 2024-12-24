# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the required dependencies
RUN pip install -r requirements.txt

# Expose the port your application runs on
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]