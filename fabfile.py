from __future__ import with_statement, print_function
from os.path import dirname, abspath, join

from fabric.api import *
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.colors import yellow, red, white, green


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
    'apps': ['virtualenv', 'python', 'npm', 'grunt']
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
    return prefix('source .virtualenv/bin/activate')


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
