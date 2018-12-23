#!/bin/bash
# Activate the virtual environment
. /appenv/bin/activate

# Download build requirements to build cache
pip download -d /build -r requirements_test.txt --no-input

# Install application test requirements
pip install --no-index -f /build -r requirements_test.txt

# Run test.sh arguments
exec $@
