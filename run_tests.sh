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


cyan_error "Running unit tests for constructs..."
(set -x; pytest tests \
    --cov=hiscores_tracker \
    --cov-config=tests/.coveragerc \
    --cov-report=html:tests/unit/.coverage)

cyan_error "Running unit tests for lambda handler libs..."
for dir in $(ls -d lambda/*)
do
    cyan_error "Testing $dir..."
    (set -x; pytest $dir \
        --doctest-modules \
        --ignore=$dir/handler.py \
        --cov=$dir \
        --cov-config=lambda/.coveragerc \
        --cov-report=html:$dir/.coverage)
done

cleanup
