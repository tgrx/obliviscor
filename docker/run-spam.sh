#!/bin/bash

echo "RUNNING SPAM"

sleep 60 # I LOVE DOCKER

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." >/dev/null 2>&1 && pwd)"

cd "${PROJECT_DIR}" || exit 1

make spam

echo "DONE: RUNNING SPAM"
