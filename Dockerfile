FROM python:3.11

WORKDIR /app

COPY requirements.txt .

ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt --no-cache-dir

COPY . .