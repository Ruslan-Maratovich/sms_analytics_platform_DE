#!/bin/bash

superset db upgrade

superset fab create-admin \
  --username admin \
  --firstname admin \
  --lastname admin \
  --email admin@test.com \
  --password admin

superset init

superset run \
  --host 0.0.0.0 \
  --port 8088
