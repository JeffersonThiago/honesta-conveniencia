FROM python:3.11-alpine3.18
LABEL maintainer="Jefferson Oliveira"

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY . /HONESTA-CONVENIENCIA
COPY ./scripts /scripts

WORKDIR /HONESTA-CONVENIENCIA
EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    apk add --no-cache gcc musl-dev libffi-dev mariadb-connector-c-dev mariadb-dev g++ pkgconfig && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp/* && \
    adduser -D django-user --disabled-password --no-create-home && \
    chown -R django-user:django-user /HONESTA-CONVENIENCIA && \
    chmod +x scripts/run.sh

ENV PATH="/scripts:/venv/bin:$PATH"

USER django-user

CMD ["sh", "/scripts/run.sh"]