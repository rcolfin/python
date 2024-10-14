FROM mambaorg/micromamba:alpine AS build

USER root

WORKDIR /

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

COPY pyproject.toml poetry.lock ./docker/nodemanager/python-wrapper ./

RUN \
    poetry install --no-interaction --no-cache --no-directory --no-root --sync --only main

FROM bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 AS runtime

ENV PATH=$PATH:/opt/conda/bin:/opt/conda/condabin \
    POETRY_VIRTUALENVS_PATH=/opt/conda/envs \
    MAMBA_ROOT_PREFIX=/opt/conda \
    MAMBA_SKIP_ACTIVATE=1

COPY --from=build /bin/micromamba /bin/micromamba
COPY --from=build /opt/conda/ /opt/conda/
COPY --from=build /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=build /pyproject.toml /poetry.lock ./
COPY --from=build /python-wrapper /bin/

RUN \
    /bin/micromamba shell init --shell bash \
    && echo 'source /usr/local/bin/_activate_current_env.sh' >> ~/.bashrc \
    && echo '/opt/conda/bin/poetry shell -C ~/' >> ~/.bashrc
