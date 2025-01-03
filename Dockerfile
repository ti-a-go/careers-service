FROM python:3.11.5-slim-bullseye as build

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFERRED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
