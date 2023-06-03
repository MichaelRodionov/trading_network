FROM python:3.11-slim

WORKDIR /retail_app

COPY poetry.lock pyproject.toml ./
COPY core/. ./core
COPY chain/. ./chain
COPY trading_network/. ./trading_network
COPY manage.py .
COPY README.md .

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev