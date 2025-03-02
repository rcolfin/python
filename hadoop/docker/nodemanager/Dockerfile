FROM mambaorg/micromamba:alpine AS build

USER root

WORKDIR /

ARG PACKAGES="python=3.13 pip uv"

ENV \
    PATH=$PATH:/opt/conda/bin/ \
    UV_NO_CACHE=1 \
    UV_PYTHON_INSTALL_DIR="/opt/conda/bin"\
    UV_PROJECT_ENVIRONMENT="/opt/conda"

# Update micromamba and install uv:
RUN \
    mkdir -p ~/.mamba/pkgs \
    && micromamba self-update -q \
    && micromamba install -qy ${PACKAGES} \
    && rm -rf /opt/conda/pkgs

COPY README.md pyproject.toml uv.lock ./docker/nodemanager/python-wrapper ./tmp/

RUN \
    cd /tmp \
    && uv sync --no-dev --locked --quiet

FROM bde2020/hadoop-nodemanager:2.0.0-hadoop3.2.1-java8 AS runtime

ENV PATH=$PATH:/opt/conda/bin:/opt/conda/condabin \
    UV_NO_CACHE=1 \
    UV_PYTHON_INSTALL_DIR="/opt/conda/bin"\
    UV_PROJECT_ENVIRONMENT="/opt/conda" \
    MAMBA_ROOT_PREFIX=/opt/conda \
    MAMBA_SKIP_ACTIVATE=1

COPY --from=build /bin/micromamba /bin/micromamba
COPY --from=build /opt/conda/ /opt/conda/
COPY --from=build /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=build /tmp/python-wrapper /bin/

RUN \
    /bin/micromamba shell init --shell bash \
    && echo 'source /usr/local/bin/_activate_current_env.sh' >> ~/.bashrc

ARG BUILD_DATE=""
ENV \
    BUILD_TIMESTAMP=${BUILD_DATE}
