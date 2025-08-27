# docker-health-check

Iterates over Docker containers and if a container is unhealthy restarts it.

## Development

### Setup Python Environment:

Run [scripts/console.sh](scripts/console.sh)

### If you need to relock:

Run [scripts/lock.sh](../scripts/lock.sh)

### Run code

Run [scripts/console.sh](../scripts/console.sh) uv run python -m docker_health_checks health-check

## Deployment

### Building

```sh
export BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
export GIT_COMMIT="$(git rev-parse --short HEAD)"
cd docker
docker compose build --pull
```

### Testing

```sh
cd docker
docker compose up
```

or

### Test Docker Image

```sh
docker run -it -v /var/run/docker.sock:/var/run/docker.sock rcolfin/docker-health-check:latest
```

```yaml
name: docker-health-check

services:
  docker-health-check:
    container_name: docker-health-check
    image: rcolfin/docker-health-check:latest
    pull_policy: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped
    command:
      - --interval
      - "30"
      - --label
      - "com.dockerhealthcheck.enable=true"
    env:
      EMAIL__SENDER:
```
