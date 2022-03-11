FROM arm32v7/python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install build-essential -y && pip install -r ./requirements.txt

COPY . .

CMD ["python3", "./app.py" ]

