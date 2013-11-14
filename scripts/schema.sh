#!/bin/sh

python manage.py schemamigration account --initial --update
python manage.py schemamigration label --initial --update
python manage.py schemamigration video --initial --update
