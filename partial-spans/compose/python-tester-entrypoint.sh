#!/usr/bin/env bash
set -e

# If the venv bin folder doesn't exist, create it and install the local package
if [ ! -f "/app/venv/bin/activate" ]; then
  echo "Creating virtual environment..."
  python -m venv /app/venv
fi

# Activate the venv
# shellcheck disable=SC1091
source /app/venv/bin/activate

# If not installed yet, or if you changed dependencies, you can re-run install
# Checking if an .egg-link or .dist-info folder exists can be a quick check
if [ ! -f "/app/venv/lib/python3.13/site-packages/opentelemetry-api.egg-link" ]; then
  echo "Installing local opentelemetry-python in editable mode..."
  pip install --no-cache-dir -r /app/otel-python-test/requirements.txt
fi

exec "$@"
