FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

ENV PYTHON_VERSION=3.9
ENV POETRY_VENV=/opt/app/.venv

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get -qq update \
    && apt-get -qq install --no-install-recommends \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python3-pip

RUN apt update && apt install -y ffmpeg libsodium23 ca-certificates git curl

RUN ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python3 && \
    ln -s -f /usr/bin/python${PYTHON_VERSION} /usr/bin/python && \
    ln -s -f /usr/bin/pip3 /usr/bin/pip

RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry

WORKDIR /opt/app
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true && \
    poetry install

COPY . .

RUN poetry run python -m pip install torch==1.13.0+cu117 -f https://download.pytorch.org/whl/torch

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/app

ENTRYPOINT ["/opt/app/manage"]
