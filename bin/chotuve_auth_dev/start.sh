#!/bin/bash

pip --disable-pip-version-check install -r requirements/dev.txt
cd src
flask db migrate
flask db upgrade
flask run --host=0.0.0.0
