# Base image
FROM python:3.11.4

# Set environment variables
ARG FASTAPI_PORT
ENV PORT=$FASTAPI_PORT
ARG FASTAPI_HOST
ENV HOST=$FASTAPI_HOST

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# Expose the port
EXPOSE $PORT

CMD uvicorn api:app --app-dir src/api --host "${HOST}" --port "${PORT}" --reload
