#!/usr/bin/env bash

set -euo pipefail

SCRIPT_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# shellcheck disable=SC1091
source "${SCRIPT_PATH}/setup-hadoop.sh"

build_docker_hadoop

start_docker_hadoop
