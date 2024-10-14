FROM mambaorg/micromamba:alpine AS build

USER root

WORKDIR /root

ARG PACKAGES="python=3.13 pip poetry"

ENV \
    PATH=$PATH:/opt/conda/bin/ \
    POETRY_VIRTUALENVS_PATH=/opt/conda/envs

# Update micromamba and install poetry:
RUN \
    mkdir -p ~/.mamba/pkgs \
    && micromamba self-update -q \
    && micromamba install -qy ${PACKAGES} \
    && rm -rf /opt/conda/pkgs

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    MAMBA_SKIP_ACTIVATE=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# Install Dependencies:
COPY poetry.lock pyproject.toml ./

RUN \
    poetry install --no-interaction --no-cache --no-directory --no-root --sync --only main

# Install Package:
COPY . ./src/

RUN \
    poetry run pip install --no-deps --no-cache-dir ./src \
    && rm -rf .cache/pip \
    && rm -rf ./src

ENTRYPOINT ["poetry", "run", "python", "-m", "docker_health_check", "health-check"]

CMD ["--interval", "30"]
