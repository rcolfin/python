#!/usr/bin/env bash

set -euo pipefail

SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# shellcheck disable=SC1091
source "${SCRIPT_PATH}/setup-hadoop.sh"

download_data_files

start_docker_hadoop

copy_project

run_map_reduce_identity
