#!/bin/bash -e

COMPOSE_DIR="./deployment"

DOCKER_COMPOSE_WEB="$COMPOSE_DIR/docker-compose.yml"

usage() {
  programname=$(basename "$0")
  echo "Usage: $programname Options"
  echo ""
  echo "Options:"
  echo "  --local-run for run all component to see ui and user test"
  echo "  --local-down for stop & remove containers"
  echo ""
  exit 1
}

build_docker() {
  echo "Create docker compose images"
  docker compose --project-directory . -f "$DOCKER_COMPOSE_WEB" up --no-deps --no-start --force-recreate --build
}

docker_compose_down() {
  echo "Docker compose down"
  docker compose --project-directory . -f "$DOCKER_COMPOSE_WEB" down
}

docker_compose_up() {
  echo "Docker compose up"
  docker compose --project-directory . -f "$DOCKER_COMPOSE_WEB" up -d
}

function main() {
  case $1 in
  --local-run)
    docker_compose_down
    build_docker
    docker_compose_up
    ;;&
  --local-down)
    docker_compose_down
    ;;&
  --local-run | --local-down) ;;
  *)
    usage
    ;;
  esac

}

main "$@"
