#!/bin/bash
set -exo pipefail

NO_TESTS_FOUND=5

>&2 echo "Running construct unit tests..."
pytest tests

for dir in $(ls -d lambda/*)
do
>&2 echo "Running tests for $dir lambda..."
pytest $dir --doctest-modules --ignore-glob=*handler.py || NO_TESTS_FOUND=$?
done

>&2 echo "Cleaning pycaches..."
py3clean hiscores_tracker lambda tests