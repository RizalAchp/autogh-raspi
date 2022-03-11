# syntax=docker/dockerfile:1
FROM arm32v7/python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "./app.py" ]

