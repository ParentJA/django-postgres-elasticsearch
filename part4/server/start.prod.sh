#!/bin/bash

python ./manage.py migrate
python ./manage.py collectstatic --clear --noinput
gunicorn --bind 0.0.0.0:8000 perusable.wsgi --workers 3
