#!/bin/bash

function run_flask() {
    echo "Start application."
    /usr/local/bin/python /app/app.py & WORKER_PID=$!
    wait $WORKER_PID
}

function run_gunicorn() {
    echo "Start application."
    gunicorn --worker-class gevent --workers 8 --bind 0.0.0.0:5001 app:app --max-requests 10000 --timeout 5 --keep-alive 5 --log-level info
}

if [[ "${VERSIONDB_ENVIRONMENT}" == "production" ]]
    then    run_gunicorn
    else    run_flask
fi
