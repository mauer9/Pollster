FROM python:3.11-slim-bookworm

ENV DJANGO_ENV=development \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWEITEBYTECODE=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.7.0 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    postgresql-client \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install

COPY . .

COPY ./entrypoint.sh /app/
ENTRYPOINT ["/app/entrypoint.sh"]
