ARG PLATFORM="linux/amd64"

FROM --platform=${PLATFORM} python:3.13-alpine AS build

ARG PACKAGE="docker-health-check"

ARG APPDIR="/application"


# Install Poetry

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

RUN \
    wget -qO - https://install.python-poetry.org | python3 -

RUN \
    mkdir -p "${POETRY_CACHE_DIR}" \
    && chmod gua+rwxs "${POETRY_CACHE_DIR}"

# Install Package:
WORKDIR "${APPDIR}"
COPY . ./

WORKDIR "${APPDIR}/${PACKAGE}"

RUN \
    poetry install --no-interaction --no-cache --no-root --quiet \
    && rm -rf ${POETRY_CACHE_DIR}/* \
    && poetry run pip install --no-deps --no-cache-dir --quiet . \
    && find -not -name 'pyproject.toml' -not -name 'poetry.lock' -delete \
    && find -type d -empty -delete \
    && rm -rf ~/.cache/pip \
    && rm -rf ~/.local

ARG BUILD_DATE=""
ENV \
    BUILD_TIMESTAMP=${BUILD_DATE}

ENTRYPOINT ["poetry", "run", "python", "-m", "docker_health_check", "health-check"]

CMD ["--interval", "30"]
