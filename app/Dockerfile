FROM python:3.6 AS build-image
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.6-slim

RUN apt-get update && \
    apt-get install --no-install-recommends -y libyaml-0-2 && \
    rm -rf /var/lib/apt/lists/* /var/cache/debconf/*-old && \
    useradd --system --user-group app

COPY --from=build-image /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
ADD . /app
RUN python /app/setup.py install