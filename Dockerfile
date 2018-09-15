FROM python:3.6-alpine

ENV FLASK_APP seed.py
ENV FLASK_CONFIG docker

RUN apk add --no-cache --update gcc build-base

WORKDIR /home/seed

COPY requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY seed.py config.py boot.sh ./
COPY app app

# run-time configuration
EXPOSE 5000
RUN ["chmod", "+x", "./boot.sh"]
ENTRYPOINT ["./boot.sh"]