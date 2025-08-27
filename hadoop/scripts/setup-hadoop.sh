#!/usr/bin/env bash

set -euo pipefail

PACKAGE_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )
PACKAGE_NAME="$(basename "${PACKAGE_PATH}")"
DOCKER_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )/docker
TEST_AREA_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/.." &> /dev/null && pwd )/test-area
LOCAL_DOCKER_PACKAGE_PATH="/tmp/${PACKAGE_NAME}"
LOCAL_DOCKER_TEST_AREA_PATH="${LOCAL_DOCKER_PACKAGE_PATH}/$(basename "${TEST_AREA_PATH}")"

HADOOP_DOCKER_COMPOSE_ENV_URL="https://raw.githubusercontent.com/big-data-europe/docker-hadoop/refs/heads/master/hadoop.env"
WORD_COUNT_URL="https://www.gutenberg.org/cache/epub/20/pg20.txt"
SOCIAL_MEDIA_CONNECTIONS_SMALL_URL="https://gist.githubusercontent.com/rcolfin/65515e06f7a9df787eb8684c0412a746/raw/911f098ce8fa55f4eaec0634805b0fb3d353f510/social_media_connections.txt"
SOCIAL_MEDIA_CONNECTIONS_LARGE_URL="https://gist.githubusercontent.com/rcolfin/72895ca575c018f82748a7e8fb4270c1/raw/5b9c35242209a8c9a0a4a9a571276c8e991cf6dd/social_media_connections_large.txt"

function log() {
    >&2 echo "${*}"
}

function ensure_test_area() {
    mkdir -p "${TEST_AREA_PATH}"
}

function download_file() {
    local URL OUTPUT_PATH

    URL="$1"
    if [ $# -ge 2 ]; then
        OUTPUT_PATH="$2"
    else
        OUTPUT_PATH=""
    fi

    [ -h "${OUTPUT_PATH}" ] || OUTPUT_PATH="${TEST_AREA_PATH}"
    OUTPUT_PATH="${OUTPUT_PATH}"/"$(basename "${URL}")"

    ensure_test_area

    log INFO "Downloading ${URL} to ${OUTPUT_PATH}"
    curl -fs --output "${OUTPUT_PATH}" "${URL}"
}

function setup_docker_hadoop() {
    download_file "${HADOOP_DOCKER_COMPOSE_ENV_URL}" "${DOCKER_PATH}"
}

function wait_for_container_ready() {
    local CONTAINER ATTEMPT RESULT
    CONTAINER="$1"

    ATTEMPT=0
    while [ $ATTEMPT -le 59 ]; do
        ATTEMPT=$(( ATTEMPT + 1 ))
        log INFO "Waiting for ${CONTAINER} to be ready (attempt: $ATTEMPT)..."
        RESULT="$(docker inspect -f '{{.State.Health.Status}}' "${CONTAINER}")"
        if [ "${RESULT}" == "healthy" ]; then
            log INFO "${CONTAINER} is ready."
            return 0
        fi

        sleep 2
    done

    log INFO "${CONTAINER} failed to launch."
    return 1
}

function start_docker_hadoop() {
    pushd "${DOCKER_PATH}" >/dev/null

    setup_docker_hadoop

    log INFO "Running docker compose -up from $PWD"

    docker compose up -d

    log INFO "Run docker compose down from $PWD to shut down."

    popd >/dev/null

    wait_for_container_ready resourcemanager
}

function build_docker_hadoop() {
    pushd "${DOCKER_PATH}" >/dev/null

    log INFO "Running docker compose build from $PWD"

    # shellcheck disable=SC2155
    export BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

    # shellcheck disable=SC2155
    export GIT_COMMIT="$(git rev-parse --short HEAD)"

    docker compose build --pull

    popd >/dev/null
}

function download_data_files() {
    download_file "${WORD_COUNT_URL}"
    download_file "${SOCIAL_MEDIA_CONNECTIONS_SMALL_URL}"
    download_file "${SOCIAL_MEDIA_CONNECTIONS_LARGE_URL}"
}

function copy_project() {
    log INFO docker exec namenode "rm -rf ${LOCAL_DOCKER_PACKAGE_PATH}"
    docker exec namenode bash -c "rm -rf ${LOCAL_DOCKER_PACKAGE_PATH}" || true

    log INFO docker cp "${PACKAGE_PATH}" "namenode:${LOCAL_DOCKER_PACKAGE_PATH}/"
    docker cp "${PACKAGE_PATH}" "namenode:${LOCAL_DOCKER_PACKAGE_PATH}/"

    docker exec namenode hadoop fs -mkdir -p input

    log INFO docker exec namenode hdfs dfs -put "${LOCAL_DOCKER_TEST_AREA_PATH}/*.txt" input
    docker exec namenode bash -c "hdfs dfs -put -f ${LOCAL_DOCKER_TEST_AREA_PATH}/*.txt input"
}

function run_map_reduce_package() {
    local PACKAGE DATAFILE
    PACKAGE="$1"
    DATAFILE="$2"

    log INFO docker exec namenode hadoop fs -rm -r output
    docker exec namenode hadoop fs -rm -r output || true

    log INFO docker exec namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -file "mapper.py" -mapper "python-wrapper mapper.py" -file "reducer.py"  -reducer "python-wrapper reducer.py" -input "input/${DATAFILE}" -output output
    docker exec -w "${LOCAL_DOCKER_PACKAGE_PATH}/hadoop/${PACKAGE}" namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar -file "mapper.py" -mapper "python-wrapper mapper.py" -file "reducer.py"  -reducer "python-wrapper reducer.py" -input "input/${DATAFILE}" -output output

    get_output
}

function get_output() {

    log INFO docker exec namenode hadoop fs -cat output/part-00000
    docker exec namenode hadoop fs -cat output/part-00000
}

function run_map_reduce_word_count() {
    run_map_reduce_package "word_count" "$(basename "${WORD_COUNT_URL}")"
}

function run_map_reduce_identity() {
    run_map_reduce_package "identity" "$(basename "${WORD_COUNT_URL}")"
}

function run_map_reduce_social_media_connect_small() {
    run_map_reduce_package "social_media_connect" "$(basename "${SOCIAL_MEDIA_CONNECTIONS_SMALL_URL}")"
}

function run_map_reduce_social_media_connect_large() {
    run_map_reduce_package "social_media_connect" "$(basename "${SOCIAL_MEDIA_CONNECTIONS_LARGE_URL}")"
}
