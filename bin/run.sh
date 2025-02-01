#!/usr/bin/env bash

gunicorn -k uvicorn.workers.UvicornWorker wsgi:app --bind 0.0.0.0:8000 --log-level=debug --workers=4