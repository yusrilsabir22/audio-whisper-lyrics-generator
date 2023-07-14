FROM python:3.9-slim

WORKDIR /opt/app

RUN pip install poetry
RUN apt update && apt install -y ffmpeg libsodium-dev ca-certificates git curl

COPY pyproject.toml poetry.lock ./
RUN python -m pip install --upgrade pip
RUN poetry config virtualenvs.create false \
    && poetry install --extras release --only main

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/app/src/py

ENTRYPOINT ["/opt/app/manage"]
