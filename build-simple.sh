#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements-simple.txt
python manage.py collectstatic --no-input
python manage.py migrate