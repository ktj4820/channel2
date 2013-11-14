#!/bin/bash

find . -name "*.pyc" -exec rm '{}' ';'
rm channel2.sqlite3
rm -fr media/*
rm -fr logs/*
python manage.py syncdb --noinput
python manage.py migrate
