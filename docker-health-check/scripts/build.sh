#!/usr/bin/env bash

set -euo pipefail

DOCKER_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/../docker" &> /dev/null && pwd )

cd "${DOCKER_PATH}"

docker compose build
