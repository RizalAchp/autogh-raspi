# syntax=docker/dockerfile:1
FROM arm32v7/python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .
CMD ["python3", "./app.py" ]

