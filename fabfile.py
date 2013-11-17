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
from contextlib import contextmanager

import datetime
from fabric.context_managers import prefix
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fabric.operations import local, put, run, prompt
from fabric.api import cd, env, sudo


env.use_ssh_config      = True

env.checkout_path       = '/tmp/django'
env.deploy_path         = '/var/www/channel2'
env.django_path         = '/var/www/channel2/django'
env.media_path          = '/var/www/channel2/media'
env.static_path         = '/var/www/channel2/static'

env.venv_path           = '/var/www/channel2/venv'
env.activate            = 'source /var/www/channel2/venv/bin/activate'

env.packages = [
    # python stuff
    'build-essential', 'python-dev', 'python-pip', 'libbz2-dev',
    # databse
    'postgresql-server-dev-9.2', 'postgresql-9.2',
    # utilites
    'cron', 'ntp', 'rsync', 'gettext', 'htop',
    # image processing
    'libjpeg8', 'libjpeg8-dev', 'libpng12-0', 'libfreetype6', 'libfreetype6-dev', 'zlib1g',
    # video processing
    'ffmpeg',
    # server
    'nginx',
]

#-------------------------------------------------------------------------------
# hosts
#-------------------------------------------------------------------------------

def production():
    """
    use channel2 as host
    """

    env.hosts = ['channel2']
    env.config = 'production'

#-------------------------------------------------------------------------------
# activate virtualenv
#-------------------------------------------------------------------------------

@contextmanager
def virtualenv():
    with cd(env.venv_path):
        with prefix(env.activate):
            yield

#-------------------------------------------------------------------------------
# setup
#-------------------------------------------------------------------------------

def setup():
    """
    installs all necessary software to get channel2 running
    """

    sudo('mkdir -p {deploy_path}'.format(**env))
    sudo('mkdir -p {deploy_path}/logs'.format(**env))
    sudo('mkdir -p {static_path}'.format(**env))
    sudo('mkdir -p {media_path}'.format(**env))
    sudo('mkdir -p {django_path}/static'.format(**env))
    sudo('chown -R www-data:www-data {deploy_path}'.format(**env))

    sudo('apt-get -y install python-software-properties')
    sudo('add-apt-repository ppa:pitti/postgresql')
    sudo('apt-get update')
    sudo('apt-get -y install {}'.format(' '.join(env.packages)))

    sudo('pip install supervisor==3.0')
    sudo('pip install virtualenv')
    sudo('touch {django_path}/static/maintenance.html'.format(**env))

    sudo('virtualenv {venv_path} --python=/usr/local/bin/python3.3'.format(**env), user='www-data')

#-------------------------------------------------------------------------------
# deploy
#-------------------------------------------------------------------------------

def deploy(tag='master'):
    """
    deploy the project to target host:

    1. checks out source locally to env.checkout_path
    2. rsync source code to remote server
    3. install requirements
    4. sync and migrate db
    """

    _checkout(tag)
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
    local('git archive {tag} | tar -x -C {checkout_path}'.format(
        tag=tag,
        checkout_path=env.checkout_path
    ))


def _fabric_marker():
    """
    Set a resource-version string to use for resource files
    """

    env.resource_version = datetime.datetime.now().strftime('%Y%m%d%H%M')
    local('sed -ire "s/fabric:resource-version/{resource_version}/g" {checkout_path}/config/{config}/localsettings.py'.format(**env))
    local('cp {checkout_path}/static/css/app.css {checkout_path}/static/css/app{resource_version}.css'.format(**env))
    local('cp {checkout_path}/static/js/app.js {checkout_path}/static/js/app{resource_version}.js'.format(**env))

def _rsync():
    """
    rsync the project from local to remote
    """

    sudo('chown -R {user}:{user} {django_path}'.format(
        user=run('whoami'),
        django_path=env.django_path
    ))

    rsync_project(
        local_dir=env.checkout_path,
        remote_dir=env.deploy_path,
        delete=True
    )

    sudo('ln -s {django_path}/config/{config}/localsettings.py {django_path}/channel2/localsettings.py'.format(**env))
    sudo('chown -R www-data:www-data {django_path}'.format(**env))

def _install_requirements():
    """
    install requirements
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            sudo('pip install -r requirements.txt')


def _syncdb_migrate():
    """
    call python manage.py syncb and python manage.py migrate
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            sudo('python manage.py syncdb --noinput', user='www-data')
            sudo('python manage.py migrate', user='www-data')
            sudo('python manage.py collectstatic --noinput', user='www-data')


#-------------------------------------------------------------------------------
# tasks
#-------------------------------------------------------------------------------

def start():
    """
    start supervisor (starts channel2)
    """

    sudo('supervisord -c {django_path}/config/{config}/supervisord.conf'.format(**env), user='www-data', pty=False)
    sudo('rm -f {static_path}/maintenance.html'.format(**env))


def stop():
    """
    stop supervisor (stops channel2)
    """

    sudo('cp {django_path}/static/maintenance.html {static_path}/maintenance.html'.format(**env), user='www-data')
    sudo('killall supervisord', warn_only=True)

def postgres_reset():
    """
    drops and re-create the database (note: the recreated database has no tables).

    Executed commands:
        drop database if exists channel2;
        drop user if exists channel2_user;
        create user channel2_user with password '<>';
        create database channel2;
        grant all privileges on database channel2 to channel2_user;
    """

    if not confirm('RESETTING THE DB. CONTINUE?', default=False):
        return

    db_password = prompt('Please enter the db password: ')
    sudo("echo 'drop database if exists channel2;' | sudo -u postgres psql")
    sudo("echo 'drop user if exists channel2_user;' | sudo -u postgres psql")

    sudo("echo \"create user channel2_user with password '{}';\" | sudo -u postgres psql".format(db_password))
    sudo("echo 'create database channel2;' | sudo -u postgres psql")
    sudo("echo 'grant all privileges on database channel2 to channel2_user;' | sudo -u postgres psql")


def postgres_update():
    """
    upload the latest postgres configuration and restart postgres
    """

    sudo('rm -f /etc/postgresql/9.2/main/postgresql.conf')
    put('config/{config}/postgresql.conf'.format(**env), '/etc/postgresql/9.2/main/postgresql.conf', use_sudo=True)
    sudo('/etc/init.d/postgresql restart')

def nginx_update():
    """
    upload the latest nginx configuration and restarts nginx
    """

    sudo('rm -f /etc/nginx/sites-enabled/default')
    sudo('rm -f /etc/nginx/nginx.conf')
    put('config/{config}/nginx.conf'.format(**env), '/etc/nginx/nginx.conf', use_sudo=True)
    sudo('/etc/init.d/nginx restart')


def manage(command):
    """
    runs 'python manage.py <command>'
    e.g. fab production command:shell --> python manage.py shell
    """

    with virtualenv():
        with cd('{django_path}'.format(**env)):
            sudo('python3.3 manage.py {}'.format(command), user='www-data')
