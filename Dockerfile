# Use an official Python runtime as a parent image
FROM python:3.8-bullseye

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install --upgrade pip
RUN pip install cmake
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV APP_NAME "Fashion Market Intelligence"

# Run app.py when the container launches
CMD ["sh", "-c", "cd src && uvicorn main:app --host 0.0.0.0 --port 8080 --log-config=log_conf.yaml" ]
