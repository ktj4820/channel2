#!/bin/bash
set -e

psql -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'channel2' AND pid <> pg_backend_pid();"
psql -c "drop database if exists channel2;"
psql -c "create database channel2;"

find . -name '*.pyc' -delete
rm -fr media/*
rm -fr logs/*

python manage.py migrate --noinput
if [ "$1" != "--empty" ]; then
    python manage.py datacreator
fi

touch channel2/settings.py
