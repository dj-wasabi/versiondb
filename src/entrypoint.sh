#!/bin/bash

GUNICORN_WORKERS=${VERSIONDB_GUNICORN_WORKERS:-8}
GUNICORN_MAX_REQUESTS=${VERSIONDB_GUNICORN_MAX_REQUESTS:-1000}
GUNICORN_TIMEOUT=${VERSIONDB_GUNICORN_TIMEOUT:-5}
GUNIRORN_KEEPALIVE=${VERSIONDB_GUNIRORN_KEEPALIVE:-5}

function run_flask() {
    echo "Start application."
    /usr/local/bin/python /app/app.py
}

function run_gunicorn() {
    echo "Start application."
    gunicorn \
        --worker-class gevent \
        --workers ${GUNICORN_WORKERS} \
        --bind 0.0.0.0:5001 \
        'app:app' \
        --max-requests ${GUNICORN_MAX_REQUESTS} \
        --timeout ${GUNICORN_TIMEOUT} \
        --keep-alive ${GUNIRORN_KEEPALIVE} \
        --log-level info
}

if [[ "${VERSIONDB_ENVIRONMENT}" == "production" ]]
    then    run_gunicorn
    else    run_flask
fi

