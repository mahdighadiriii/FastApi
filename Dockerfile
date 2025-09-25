FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    && apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-setuptools \
    python3-gevent \
    build-essential \
    libssl-dev \
    libpq-dev \
    libffi-dev \
    gcc \
    libevent-dev \
    vim \
    curl \
    iputils-ping \
    libjpeg-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN find . -name "*.po" -exec msgfmt {} -o {}.mo \; 2>/dev/null || true

COPY . /app
