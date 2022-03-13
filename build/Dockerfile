FROM python:3.8-slim-buster

RUN apt update
RUN apt install sqlite3

ENV PYTHONPATH="${PYTHONPATH}:/project"

COPY requirements.txt /tmp
RUN python3 -m pip install -r /tmp/requirements.txt

COPY src /project