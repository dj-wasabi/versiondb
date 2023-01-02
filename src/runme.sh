#!/bin/bash

function run_me() {
    echo "Start application."
    /usr/local/bin/python /app/app.py & WORKER_PID=$!
    wait $WORKER_PID
}

# function stop_me() {
#     echo "Stopping application and deregister service in Consul."
#     /usr/local/bin/python deregister.py
#     exit 1
# }

# trap 'stop_me' TERM

if [[ "${FLASK_ENV}" == "test" ]]
    then    sleep 1
            pip install -r /app/requirements-dev.txt
            python manage.py test
    else    run_me
fi