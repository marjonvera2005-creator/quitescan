#!/usr/bin/env bash
# Install system dependencies
apt-get update
apt-get install -y libpq-dev python3-dev

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Django setup
python manage.py collectstatic --no-input
python manage.py migrate