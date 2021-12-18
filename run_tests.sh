#!/bin/bash
set -eo pipefail

CYAN='\033[1;36m'
NC='\033[0m'

cyan_error() {
    >&2 echo -e "${CYAN}${1}${NC}"
}


cleanup() {
    set +x; cyan_error "Cleaning pycaches..."
    set -x; py3clean hiscores_tracker lambda tests
}
trap 'cleanup' ERR


cyan_error "Running unit tests..."
(set -x; pytest tests lambda \
    --doctest-modules \
    --ignore-glob=lambda/*/handler.py \
    --cov=hiscores_tracker \
    --cov=lambda \
    --cov-report=html:.coverage_html
)

cleanup
