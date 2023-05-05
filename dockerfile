# Use the official Python image as the base image
FROM python:3.9-slim

RUN echo "Starting Dockerfile"

# Set the working directory
WORKDIR /app

RUN echo "Installing system deps and Chrome"

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl unzip gnupg \
    libx11-xcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxi6 \
    libxtst6 libnss3 libcups2 libxss1 libxrandr2 libasound2 libpangocairo-1.0-0 \
    libatk1.0-0 libgtk-3-0 libgdk-pixbuf2.0-0 libatspi2.0-0 \
    && \
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "Installing Chrome WebDriver"

# Install Chrome WebDriver
RUN CHROME_VERSION=$(google-chrome --product-version) && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION) && \
    curl -sS -o /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

RUN echo "Installing Python deps"

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "Copying the rest of the application code"

# Copy the rest of the application code to the container
COPY . .

RUN echo "Expose port"

# Expose the API port
EXPOSE 8000

RUN echo "Starting the application"

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]