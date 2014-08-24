from __future__ import with_statement, print_function
from os.path import dirname, abspath, join
from os.path import exists as os_exists

from fabric.api import *
from fabric.context_managers import settings, cd
from fabric.contrib.files import exists
from fabric.colors import yellow, red, white, green
from fabric.operations import local


#
# GLOBALS
#
env.LOCAL_PATH = dirname(abspath(__file__))

#
# HOSTS
#
HOSTS = {
    'local': {
        'host': '127.0.0.1',
        'path': env.LOCAL_PATH,
    },
    'dev': {
        'host': 'dev',
        'path': '~',
        'user': 'app',
    }
}

if not env.hosts:
    env.hosts = ['local']

# Doctor checkups
DOCTOR = {
    'apps': ['virtualenv', 'python', 'npm', 'grunt', 'bower']
}


#
# HELPERS
#
def get_host_string(host_config):
    host_string = ''
    if 'user' in host_config:
        host_string += '{}@'.format(host_config['user'])

    host_string += host_config['host']

    if 'port' in host_config:
        host_string += ':{}'.format(host_config['port'])

    return host_string


def get_host_app_environment():
    """
    Get remote $ENVIRONMENT variable value.
    Default: local
    """
    # In case we're setting up a new host we need this defined
    app_environment = 'local'
    try:
        ssh_io = run('echo -e "\n$ENVIRONMENT"', quiet=True).split()[1]
    except IndexError:
        ssh_io = 'local'
    if ssh_io and exists(join(env.LOCAL_PATH, 'config', ssh_io)):
        app_environment = ssh_io

    return app_environment


#
# CONTEXT MANAGERS
#
def virtualenv():
    """
    Activates virtualenv first
    """
    return prefix(
        'source {}/.virtualenv/bin/activate'.format(
            env.host_config['path']
        )
    )


#
# DECORATORS
#
def task_environment(method):
    """
    Retrieves host based configuration and app_environment from the host
    and automatically CDs into the specified path
    """
    def wrapper(*args, **kwargs):
        env.host_config = HOSTS[env.host]
        with settings(host_string=get_host_string(env.host_config)):
            env.appenv = get_host_app_environment()

            with cd(env.host_config['path']):
                return method(*args, **kwargs)
    return wrapper


#
# TASKS
#
@task_environment
@task
def setup_environment():
    """
    Prepares environment for the application
    """
    execute(setup_virtualenv)
    execute(setup_tools)
    execute(setup_database)


@task_environment
@task
def setup_virtualenv():
    """
    Creates or updates a virtualenv
    """
    if not exists('.virtualenv'):
        print(yellow('Create virtualenv'))
        run('virtualenv-2.7 .virtualenv')

    with virtualenv():
        print(yellow('Installing requirements'))
        run('pip install -r config/{}/requirements.txt --use-mirrors'.format(
            env.appenv))


@task_environment
@task
def setup_tools():
    # Setup frontend tools
    print(yellow('Installing npm dependencies'))
    run('npm install')


@task_environment
@task
def setup_database():
    """
    Create or update the database
    """
    with virtualenv():
        print(yellow('SyncDB'))
        run('python manage.py syncdb')
        print(yellow('Migrate'))
        run('python manage.py migrate')


@task_environment
@task
def set_environment():
    env_type = prompt('Environment type?')
    bashrc = run('cat $HOME/.bashrc', quiet=True)
    if 'export ENVIRONMENT=`cat $HOME/.environment`' not in bashrc:
        print(red('Error: .bashrc is not properly configured!'))
        run("echo export ENVIRONMENT=\$\(cat $HOME/.environment\) "
            ">> .bash_profile")
    run('echo {} > .environment'.format(env_type))


@task_environment
@task
def shell():
    """
    Opens a shell to the given host
    """
    open_shell('cd {}'.format(env.host_config['path']))


@task_environment
@task
def doctor():
    print(yellow('Checking for software:'))
    for app in DOCTOR['apps']:
        print(white('{}'.format(app)), end=': ')
        check = run('which {}'.format(app), quiet=True)
        if check.succeeded:
            print(green('present'))
        else:
            print(red('not present'))


#
#   LOCAL ONLY
#
@task_environment
@task
@hosts(['local'])
def runserver():
    """
    Executes local development server
    """
    with virtualenv():
        run('python manage.py runserver 0.0.0.0:8000')


@task_environment
@task
def clean_pyc():
    run('find . -name "*.pyc" -exec rm -rf {} \;')


@task_environment
@task
@hosts(['local'])
def rungrunt():
    """
    Executes grunt
    """
    run('grunt --force')


@task_environment
@task
@hosts(['local'])
def makemessages():
    """
    Executes django-admin makemessages where needed
    """
    with cd('shelfzilla'):
        if not exists('locale'):
            run('mkdir locale')
        with virtualenv():
            run('django-admin.py makemessages -l es', quiet=True)

    """
    apps = ['homepage', 'landing', 'manga', 'users']
    for app in apps:
        with cd('shelfzilla/apps/{}'.format(app)):
            if not exists('locale'):
                run('mkdir locale')
            with virtualenv():
                run('django-admin.py makemessages -l es', quiet=True)
    """

@task_environment
@task
def clean_backups(BCK_BASE_PATH='/backups/sql', DAYS='30'):
    """
    This function clean old backups from backup base path
    """
    print(white("\tCleaning oldest backups..."))
    with settings(hide('warnings', 'running', 'stdout', 'stderr')):
        local('find %s -mtime +%s -exec rm -rf {} \;' % (BCK_BASE_PATH, DAYS))

@task_environment
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
