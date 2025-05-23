#!/bin/sh

source .venv/bin/activate
gunicorn -b ":${PORT}" "pyrun:create_app()"
