#!/usr/bin/env bash

set -euo pipefail

function log() {
    >&2 echo "${*}"
}

BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
GIT_COMMIT="$(git rev-parse --short HEAD)"

log "BUILD_DATE=${BUILD_DATE}"
log "GIT_COMMIT=${GIT_COMMIT}"

if [ -n "${GITHUB_ENV+x}" ]; then
    echo "BUILD_DATE=${BUILD_DATE}" >> $GITHUB_ENV
    echo "GIT_COMMIT=${GIT_COMMIT}" >> $GITHUB_ENV
fi
