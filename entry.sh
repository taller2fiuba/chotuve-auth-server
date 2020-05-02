#!/bin/bash

flask db migrate
flask db upgrade
exec gunicorn --bind 0.0.0.0:$PORT wsgi

