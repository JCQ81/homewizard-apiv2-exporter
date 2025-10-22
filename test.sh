#!/bin/bash

gunicorn homewizard-apiv2-exporter:app --bind :9898 --workers 1 --threads 1 2>&1 &

sleep 0.5
curl http://localhost:9898/metrics?target=$1

killall gunicorn

sleep 0.5
exit
