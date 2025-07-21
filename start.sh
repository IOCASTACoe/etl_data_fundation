#!/bin/bash

source .venv/bin/activate
mkdir -p /opt/logs
mkdir -p /opt/temp
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

