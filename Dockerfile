# Use the official Python image as a base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container


# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project into the container
COPY . .

# Set entrypoint
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]