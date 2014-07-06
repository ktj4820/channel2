#-------------------------------------------------------------------------------
# This is not a docstring because we don't want fabric to print this comment.
#
# Get started by typing `fab -l` into your terminal.
#
# Basic usage:
#   fab <host> <command>
#
# Example:
#   fab qa setup        # this sets up the QA server
#   fab qa deploy       # this deploys the master branch to QA server
#-------------------------------------------------------------------------------

import datetime
from contextlib import contextmanager

from fabric.context_managers import prefix
from fabric.contrib.files import exists
from fabric.contrib.project import rsync_project
from fabric.operations import local, run, get, prompt, put, sudo
from fabric.api import cd, env, run


env.use_ssh_config      = True

env.checkout_path       = '/tmp/django'
env.deploy_path         = '/var/www/channel2'
env.django_path         = '/var/www/channel2/django'
env.static_path         = '/var/www/channel2/static'.format(**env)

env.venv_path           = '/var/www/channel2/venv'
env.activate            = 'source /var/www/channel2/venv/bin/activate'

env.hosts               = ['channel2']

#-------------------------------------------------------------------------------
# activate virtualenv
#-------------------------------------------------------------------------------

@contextmanager
def virtualenv():
    with cd(env.venv_path):
        with prefix(env.activate):
            yield

#-------------------------------------------------------------------------------
# install python
#-------------------------------------------------------------------------------


def install_python():
    """
    builds and installs python
    """

    VERSION = '3.4.1'

    run('wget http://legacy.python.org/ftp//python/{VERSION}/Python-{VERSION}.tgz'.format(VERSION=VERSION))
    run('tar xvf ./Python-{VERSION}.tgz'.format(VERSION=VERSION))
    with cd('./Python-{VERSION}'.format(VERSION=VERSION)):
        run('rm -fr /opt/python3.4')
        run('./configure --prefix=/opt/python3.4 --with-bz2')
        run('make')
        run('make install')
        run('rm -f /usr/local/bin/python3.4')
        run('ln -s /opt/python3.4/bin/python3.4 /usr/local/bin/python3.4')
    run('rm -f Python-{VERSION}.tgz'.format(VERSION=VERSION))
    run('rm -fr Python-{VERSION}'.format(VERSION=VERSION))
    run('rm -fr {venv_path}'.format(**env))
    sudo('virtualenv {venv_path} --python=/usr/local/bin/python3.4'.format(**env), user='www-data')


#-------------------------------------------------------------------------------
# deploy
#-------------------------------------------------------------------------------


def deploy(tag):
    """
    deploy the project to target host:

    1. checks out source locally to env.checkout_path
    2. rsync source code to remote server
    3. install requirements
    4. sync and migrate db
    """

    env.config = 'default'

    _checkout(tag)
    _compile_static()
    _fabric_marker()
    stop()
    _rsync()
    _install_requirements()
    _syncdb_migrate()
    start()


#-------------------------------------------------------------------------------


def _checkout(tag):
    """
    Checkout source locally
    """

    local('rm -fr {checkout_path}'.format(**env))
    local('mkdir -p {checkout_path}'.format(**env))
    local('git fetch')
    local('cd .. && git archive {tag} | tar -x -C {checkout_path}'.format(
        tag=tag,
        checkout_path=env.checkout_path
    ))


def _compile_static():
    """
    compile less files into css files for deployment
    """

    local('cd {checkout_path} && lessc -x static/css/app.less > static/css/app.css'.format(**env))


def _fabric_marker():
    """
    Set a resource-version string to use for resource files
    """

    env.resource_version = datetime.datetime.now().strftime('%Y%m%d%H%M')
    local('sed -ire "s/fabric:resource-version/{resource_version}/g" {checkout_path}/config/{config}/localsettings.py'.format(**env))


def _rsync():
    """
    rsync the project from local to remote
    """

    run('chown -R {user}:{user} {django_path}'.format(
        user=run('whoami'),
        django_path=env.django_path
    ))

    rsync_project(
        local_dir=env.checkout_path,
        remote_dir=env.deploy_path,
        delete=True
    )

    run('ln -s {django_path}/config/{config}/localsettings.py {django_path}/channel2/localsettings.py'.format(**env))
    run('chown -R www-data:www-data {django_path}'.format(**env))
    run('chown www-data:www-data {deploy_path}'.format(**env))


def _install_requirements():
    """
    install requirements
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            run('rm -fr {venv_path}/build')
            run('pip install -r requirements.txt')


def _syncdb_migrate():
    """
    call python manage.py syncb and python manage.py migrate
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            run('python manage.py migrate')
            sudo('python manage.py collectstatic --noinput', user='www-data')


#-------------------------------------------------------------------------------
# tasks
#-------------------------------------------------------------------------------


def start():
    """
    start supervisor (starts channel2)
    """

    run('service supervisor start')
    run('rm -f {static_path}/maintenance.html'.format(**env))


def stop():
    """
    stop supervisor (stops channel2)
    """

    if exists('{django_path}/static/maintenance.html'.format(**env)):
        sudo('cp {django_path}/static/maintenance.html {static_path}/maintenance.html'.format(**env), user='www-data')
    run('killall supervisord', warn_only=True)


def manage(command):
    """
    runs 'python manage.py <command>'
    e.g. fab production command:shell --> python manage.py shell
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            sudo('python manage.py {}'.format(command), user='www-data')


def dump_db():
    """
    generate a SQL dump of the db
    """

    db = {
        'HOST': 'localhost',
        'USER': 'channel2_user',
        'NAME': 'channel2',
        'PORT': '5432'
    }

    run('pg_dump -cO -h {HOST} -U {USER} {NAME} -p {PORT} > dump.sql'.format(**db))
    run('rm -f dump.sql.gz')
    run('gzip dump.sql')
    get('dump.sql.gz', 'dump.sql.gz')
