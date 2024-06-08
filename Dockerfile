# Use an official Python runtime as a parent image.
# See https://hub.docker.com/_/python for more information.
# To understand docker image tags, see https://forums.docker.com/t/differences-between-standard-docker-images-and-alpine-slim-versions/134973
FROM python:slim-bullseye

# Install system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # deps for python packages
    build-essential \
    python3-dev \
    libffi-dev \
    g++ \
    && apt-get clean

# Set the working directory to /opt/app
WORKDIR /opt/app

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file
COPY requirements.txt .

# Install dependencies from the requirements file
RUN pip install -r requirements.txt

# Copy source package
ADD src .

# Copy application entrypoint
COPY main.py .

# Keep container idle
CMD tail -f /dev/null
