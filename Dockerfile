FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /usr/

RUN pip install -r /usr/requirements.txt

COPY . /usr/project