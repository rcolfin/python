ARG PLATFORM="linux/amd64"

FROM --platform=${PLATFORM} ghcr.io/astral-sh/uv:python3.13-alpine AS build

ARG PACKAGE="docker-health-check"

ARG APPDIR="/application"


# Setup uv

ENV \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_NO_CACHE=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local"

# Install Package:
WORKDIR "${APPDIR}"
COPY . ./

WORKDIR "${APPDIR}/${PACKAGE}"

RUN \
    uv sync --no-dev --locked --quiet \
    && uv run --no-sync pip install --no-deps --no-cache-dir --quiet . \
    && rm -rf ./*

ARG BUILD_DATE=""
ENV \
    BUILD_TIMESTAMP=${BUILD_DATE}

ENTRYPOINT ["python", "-m", "docker_health_check", "health-check"]

CMD ["--interval", "30"]
