#!/bin/bash

pip install -r requirements/dev.txt
cd src
flask db migrate
flask db upgrade
flask run --host=0.0.0.0
