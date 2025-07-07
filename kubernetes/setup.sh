#!/usr/bin/env bash

set -euo pipefail

minikube start --driver=docker

docker version

# para ejecutar kubectl desde mininikube
# alias kubectl="minikube kubectl --"

# minikube kubectl -- apply --filename deployments.yaml
