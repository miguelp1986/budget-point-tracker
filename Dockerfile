# Base image
FROM python:3.11.4

# Set environment variables
ARG FASTAPI_PORT
ENV PORT=$FASTAPI_PORT
ARG FASTAPI_HOST
ENV HOST=$FASTAPI_HOST

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the current directory contents into the container
COPY . /app

# Expose the port
EXPOSE $PORT

# Run FastAPI application with uvicorn
CMD uvicorn api:app --app-dir src/api --host "${HOST}" --port "${PORT}" --reload
