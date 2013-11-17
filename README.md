Channel 2
=========

Channel 2 is the second version of Derek's Channel.

Development Environment Setup
-----------------------------

Developing for Channel 2 version 3 on OS X requires:

* Xcode with GCC compiler installed
* [Python 3.3+](http://www.python.org/)
* [npm](https://npmjs.org/)
* [less.app](http://incident57.com/less/)

Start by installing `pip`

    > sudo easy_install pip
    > sudo pip install virtualenv virtualenvwrapper
    > mkdir ~/.envs

Add the following lines to `.bash_profile`

    export WORKON_HOME=~/.envs
    source /usr/local/bin/virtualenvwrapper.sh

Restart your terminal, then create a new virtual environment. Check that the installed version are correct.

    > mkvirtualenv --python=python3.3 channel2
    (channel2) > python --version
    Python 3.3.2
    (channel2) > pip --version
    pip 1.4.1 from ... (python 3.3)

The `(channel2)` prefix indicates the `channel2` virtual environment is active. To work a virtual environment

    > workon channel2
    (channel2) >

Deployment Environment Setup
----------------------------

