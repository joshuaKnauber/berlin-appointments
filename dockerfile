# Use the official Selenium Standalone Chrome image as the base image
FROM selenium/standalone-chrome:4.1.0

# Set the working directory
WORKDIR /app

# Set the environment variable for Python output buffering
ENV PYTHONUNBUFFERED=1

# Install Python and other required packages
USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3.9 python3-pip && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the API port
EXPOSE 8000

# Expose the selenium port
EXPOSE 4444

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
