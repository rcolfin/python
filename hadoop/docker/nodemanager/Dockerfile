FROM mambaorg/micromamba:alpine AS build

ARG PACKAGES="python=3.13 poetry"

WORKDIR /application

ENV POETRY_VIRTUALENVS_PATH=/opt/conda/envs

RUN \
    micromamba self-update -q \
    && micromamba install -qy ${PACKAGES}

COPY pyproject.toml poetry.lock ./

RUN \
    /opt/conda/bin/poetry install --no-interaction --no-cache --no-directory --sync --only main

FROM bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 AS runtime

ENV PATH=$PATH:/opt/conda/bin:/opt/conda/condabin \
    POETRY_VIRTUALENVS_PATH=/opt/conda/envs \
    MAMBA_ROOT_PREFIX=/opt/conda \
    MAMBA_SKIP_ACTIVATE=1

COPY --from=build /bin/micromamba /bin/micromamba
COPY --from=build /opt/conda/ /opt/conda/
COPY --from=build /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=build /application/ ./

RUN \
    /bin/micromamba shell init --shell bash --root-prefix=$MAMBA_ROOT_PREFIX \
    && echo 'source /usr/local/bin/_activate_current_env.sh' >> ~/.bashrc \
    && echo '/opt/conda/bin/poetry shell -C ~/' >> ~/.bashrc
