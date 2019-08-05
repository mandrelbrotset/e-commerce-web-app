FROM python:3.7-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY flask_settings flask_settings

# install and configure nginx as proxy server
RUN apt-get update \
    && apt-get install nginx curl -y \
    && rm /etc/nginx/sites-enabled/default \
    && cp flask_settings /etc/nginx/sites-enabled/flask_settings \
    && cp flask_settings /etc/nginx/sites-available/flask_settings

COPY . .

LABEL maintainer="Sheriff Olaoye" \
      version="1.0"

RUN chmod +x startup-script.sh
ENTRYPOINT ["/app/startup-script.sh"]

CMD gunicorn --log-level=info --bind unix:/tmp/socket rest-api:app
