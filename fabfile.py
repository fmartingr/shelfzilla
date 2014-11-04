from __future__ import with_statement, print_function
from os.path import dirname, abspath, join
from os.path import exists as os_exists
from os import getcwd

from fabric.api import *
from fabric.context_managers import settings, cd
from fabric.contrib.files import exists
from fabric.colors import yellow, red, white, green
from fabric.operations import local


#
# GLOBALS
#
env.LOCAL_PATH = dirname(abspath(__file__))


if not env.hosts:
    env.hosts = ['localhost']

# Doctor checkups
DOCTOR = {
    'apps': ['virtualenv', 'python', 'npm', 'grunt', 'bower']
}


#
# CONTEXT MANAGERS
#
def virtualenv():
    """
    Activates virtualenv first
    """
    return prefix('source .virtualenv/bin/activate')


#
# TASKS
#
@task
def setup_environment():
    """
    Prepares environment for the application
    """
    execute(setup_virtualenv)
    execute(setup_tools)
    execute(setup_database)


@task
def setup_virtualenv():
    """
    Creates or updates a virtualenv
    """
    print(yellow('Create virtualenv'))
    local('virtualenv-2.7 .virtualenv')

    with virtualenv():
        print(yellow('Installing requirements'))
        local('pip install -r config/local/requirements.txt')


@task
def setup_tools():
    # Setup frontend tools
    print(yellow('Installing npm dependencies'))
    local('npm install')


@task
def setup_database():
    """
    Create or update the database
    """
    with virtualenv():
        print(yellow('SyncDB'))
        local('python manage.py syncdb')
        # print(yellow('Migrate'))
        # local('python manage.py migrate')


@task
def doctor():
    print(yellow('Checking for software:'))
    for app in DOCTOR['apps']:
        print(white('{}'.format(app)), end=': ')
        check = local('which {}'.format(app), quiet=True)
        if check.succeeded:
            print(green('present'))
        else:
            print(red('not present'))


#
#   LOCAL ONLY
#
@task
@hosts(['localhost'])
def runserver():
    """
    Executes local development server
    """
    with virtualenv():
        local('python manage.py runserver 0.0.0.0:8000')


@task
def clean_pyc():
    local('find . -name "*.pyc" -exec rm -rf {} \;')


@task
@hosts(['localhost'])
def rungrunt():
    """
    Executes grunt
    """
    local('grunt --force')


@task
@hosts(['localhost'])
def makemessages():
    """
    Executes django-admin makemessages where needed
    """
    with virtualenv():
        local('cd shelfzilla && django-admin.py makemessages -l es')


#
#   BACKUPS
#
@task
def clean_backups(BCK_BASE_PATH='/backups/sql', DAYS='30'):
    """
    This function clean old backups from backup base path
    """
    print(white("\tCleaning oldest backups..."))
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        local('find %s -mtime +%s -exec rm -rf {} \;' % (BCK_BASE_PATH, DAYS))


@task
def backup():
    """
    This function makes a PostgreSQL Backup and put it in backup base path
    """
    import time

    BCK_BASE_PATH = '/backups/sql'
    DATABASE = "shelfzilla"
    print(white("\n\tMaking backup of [%s] database" % DATABASE))
    with settings(hide('running')):
        if not os_exists(BCK_BASE_PATH + '/' + time.strftime("%d_%m_%Y")):
            local('mkdir -p %s' % BCK_BASE_PATH + '/' + time.strftime("%d_%m_%Y"))

        with lcd(BCK_BASE_PATH + '/' + time.strftime("%d_%m_%Y")):
            local('pg_dump %s | gzip > %s.gz' %
                (DATABASE, "shelfzilla_" + time.strftime("%H:%M_%d_%m_%Y")) )

    clean_backups()
