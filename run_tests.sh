#!/bin/bash
set -exo pipefail

NO_TESTS_FOUND=5

>&2 echo "Running unit tests for constructs..."
pytest tests --cov=hiscores_tracker --cov-report=term-missing --cov-fail-under=0

>&2 echo "Running unit tests for lambda handler libs..."
for dir in $(ls -d lambda/*)
do
>&2 echo "Testing $dir..."
pytest $dir --doctest-modules --ignore-glob=*handler.py --cov=$dir --cov-report=term-missing --cov-fail-under=0 || NO_TESTS_FOUND=$?
done

>&2 echo "Cleaning pycaches..."
py3clean hiscores_tracker lambda tests