FROM python:3.13-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /usr/src/app/
