#!/usr/bin/env bash

set -euo pipefail

DOCKER_PATH=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )/../docker" &> /dev/null && pwd )

# shellcheck disable=SC2155
export BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# shellcheck disable=SC2155
export GIT_COMMIT="$(git rev-parse --short HEAD)"

cd "${DOCKER_PATH}"

docker compose build --pull
