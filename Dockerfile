# syntax=docker/dockerfile:1
FROM arm32v7/python:3.9-slim-buster

WORKDIR /usr/src/app/
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["bash", "-c", "python", "./app.py" ]]

