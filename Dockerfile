FROM python:3.6-alpine

RUN apk add --no-cache --update gcc build-base postgresql-dev python3-dev

WORKDIR /home/seed

COPY requirements.txt ./
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY seed.py config.py boot.sh ./

# run-time configuration
EXPOSE 5001
RUN ["chmod", "+x", "./boot.sh"]

ENV FLASK_APP seed.py
ENV FLASK_CONFIG docker

ENTRYPOINT ["./boot.sh"]