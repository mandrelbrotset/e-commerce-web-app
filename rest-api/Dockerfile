FROM python:3.7-alpine3.10

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Sheriff" \
      version="1.0"

CMD env FLASK_APP=rest-api.py flask run --host=0.0.0.0 --port=5002


