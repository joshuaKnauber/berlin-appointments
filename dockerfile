# Use the official Python image with buster as the base image
FROM python:3.9-slim-buster

# Install dependencies required for Chrome and ChromeDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends wget gnupg2 curl unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends google-chrome-stable && \
    rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install ChromeDriver using Puppeteer's installation script
RUN PUPPETEER_PRODUCT=chrome PUPPETEER_SKIP_DOWNLOAD=true \
    pip install --no-cache-dir -U puppeteer && \
    python -m playwright install

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose the API port
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
