FROM python:3.12.2-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends --yes \
    tzdata \
    cron \
    build-essential \
    python3-dev \
    python2.7-dev \
    libldap2-dev \
    libsasl2-dev \
    slapd \
    ldap-utils \
    tox \
    lcov \
    valgrind \
    libmagic1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/log/web

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../.. .

ENTRYPOINT ["bash", "./run-backend.sh"]
