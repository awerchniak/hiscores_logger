#!/bin/bash
set -exo pipefail

NO_TESTS_FOUND=5

>&2 echo "Running unit tests for constructs..."
pytest tests \
    -v \
    --cov=hiscores_tracker \
    --cov-report=term-missing \
    --cov-fail-under=0 \
    --cov-report=html:tests/.coverage

>&2 echo "Running unit tests for lambda handler libs..."
for dir in $(ls -d lambda/*)
do
>&2 echo "Testing $dir..."
pytest $dir \
    -v \
    --doctest-modules \
    --ignore=$dir/handler.py \
    --cov=$dir \
    --cov-report=term-missing \
    --cov-fail-under=0 \
    --cov-report=html:$dir/.coverage \
    || NO_TESTS_FOUND=$?
done

>&2 echo "Cleaning pycaches..."
py3clean hiscores_tracker lambda tests