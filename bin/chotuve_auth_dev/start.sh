#!/bin/bash

pip --disable-pip-version-check install -r requirements/dev.txt
bin/wait-for-db
cd src
flask db upgrade
flask run --host=0.0.0.0
