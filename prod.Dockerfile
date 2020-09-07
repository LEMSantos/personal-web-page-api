FROM python:3.8-slim-buster

ENV PATH ${PATH}:/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /app

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y apt-utils

RUN apt-get install -y gnupg \
  build-essential

RUN pip install setuptools wheel cython

COPY requirements.txt ./

RUN pip install -r requirements.txt

ADD config ./config

RUN orator migrate -c config/database.py

RUN python -m personalwebpageapi token --create
