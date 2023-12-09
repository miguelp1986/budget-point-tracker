# Base image
FROM python:3.12.0

# Set environment variables
ARG TEST_FASTAPI_PORT
ENV PORT=$TEST_FASTAPI_PORT
ARG TEST_FASTAPI_HOST
ENV HOST=$TEST_FASTAPI_HOST

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

# Expose the port
EXPOSE $PORT

CMD uvicorn src.api.api:app --host "${HOST}" --port "${PORT}" --reload
