#!/bin/sh
set -e
python pypi_scout/scripts/setup.py --no-upsert
uvicorn pypi_scout.api.main:app --host 0.0.0.0 --port 8000
