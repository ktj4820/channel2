#!/bin/bash
set -e

psql -c "drop database if exists channel2;"
psql -c "create database channel2;"

rm -fr __pycache__
rm -fr media/*
rm -fr logs/*
python manage.py migrate --noinput
if [ "$1" != "--empty" ]; then
    python channel2/datacreator.py
fi
