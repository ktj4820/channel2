Channel 2
=========

Channel 2 is a personal video hosting service. It allows you to upload, tag and share videos and watch them on other devices.

See http://channel2.derekkwok.net

Development Environment Setup
-----------------------------

You will need the following:

- Python 3.4+
- [PostgreSQL](http://www.postgresql.org/)
- [npm](https://www.npmjs.org/)

Start by creating a python virtual environment:

	$ mkvirtualenv channel2 --python=/usr/local/bin/python3
	(channel2) $ 

The `(channel2)` prefix indicates that a virtual environment called "channel2" is being used. Next, check that you have the required version of Python:

	(channel2) $ python --version
	Python 3.4.3
	(channel2) $ pip --version
	pip 1.5.6 from /Users/.../site-packages (python 3.4)

Install the project requirements:

	(channel2) $ ./scripts/upgrade.sh

Create the database and populate it with some test data:

	(channel2) $ ./scripts/autosync.sh

Create `imagepress/localsettings.py` with the following:
	
	DEBUG = True

Run the server:

	(channel2) $ python manage.py runserver


Less Styles Compilation
-----------------------

Gulp is used to watch and autorun less compilation:

    $ npm install
    $ gulp
