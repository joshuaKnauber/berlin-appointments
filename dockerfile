FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    apt-get install -yqq unzip && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Expose the FastAPI port
EXPOSE 8000

# Copy the Python files to the working directory
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
