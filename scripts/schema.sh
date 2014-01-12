#!/bin/sh

python manage.py schemamigration account --auto
python manage.py schemamigration label --auto
python manage.py schemamigration video --auto
