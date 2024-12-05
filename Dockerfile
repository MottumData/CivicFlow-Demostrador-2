FROM python:3.11-slim-bookworm
LABEL authors="Arturo Ortiz"

WORKDIR /app

EXPOSE 8501

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -r requirements.txt

COPY . /app
 
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]