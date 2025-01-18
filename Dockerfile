FROM python:3.13-alpine3.21
LABEL maintainer="Jefferson Oliveira"

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache gcc musl-dev libffi-dev mariadb-connector-c-dev pkgconfig

COPY ./requirements.txt /tmp/requirements.txt
COPY . /HONESTA-CONVENIENCIA

WORKDIR /HONESTA-CONVENIENCIA
EXPOSE 8000


RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser -D django-user

ENV PATH="/venv/bin:$PATH"

USER django-user