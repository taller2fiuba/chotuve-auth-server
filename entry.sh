#!/bin/bash

wait-for-db
flask db upgrade
exec gunicorn --bind 0.0.0.0:$PORT wsgi

