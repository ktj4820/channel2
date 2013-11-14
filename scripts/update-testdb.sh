#!/bin/bash

find . -name "*.pyc" -exec rm '{}' ';'
rm channel2.sqlite3
rm -fr media/*
rm -fr logs/*
python manage.py syncdb --noinput
python manage.py migrate
python channel2/datacreator.py test
cp channel2.sqlite3 data/test.sqlite3
