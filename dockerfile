# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl unzip gnupg \
    libxss1 libappindicator1 libindicator7 libpango1.0-0 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 libxrandr2 libxrender1 libxslt1.1 libxtst6 libnss3 libcups2 libxkbcommon0 libxext6 libx11-xcb1 libasound2 libatk1.0-0 libatspi2.0-0 libgdk-pixbuf2.0-0 libgtk-3-0 libpangocairo-1.0-0 libgbm1 && \
    curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome WebDriver
RUN CHROME_VERSION=$(google-chrome --product-version) && \
    CHROME_MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1) && \
    CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR_VERSION) && \
    curl -sS -o /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

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