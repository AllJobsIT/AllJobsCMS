from contextlib import contextmanager

from fabric.api import env, cd, roles, execute
from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import sudo

env.roledefs = {
    "dev": {
        'hosts': ['157.90.183.254:522'],
        'branch': 'master',
        'user': 'deploy',
        'compose_file': './docker-compose.yml',
        'compose_service': '',
        'project_path': '/home/deploy/AllJobsCMS'
    },
}


def deploy_process(role_config, rebuild=''):
    with project_context(role_config):
        sudo(
            "git checkout -f && git checkout {branch} && git pull origin {branch}".format(branch=role_config['branch']))
        if rebuild == 'rebuild':
            sudo('docker compose -f {} build -q'.format(role_config['compose_file']))
        sudo('docker compose -f {} down 2>/dev/null'.format(role_config['compose_file']))
        sudo('docker compose -f {} up -d --build 2>/dev/null'.format(role_config['compose_file']))
        sudo('docker system prune -a -f')
        # sudo('docker compose -f {} exec {} python manage.py collectstatic --noinput --clear'.format(role_config['compose_file'], role_config['compose_service']))
        # sudo('docker compose -f {} exec {} python manage.py migrate'.format(role_config['compose_file'], role_config['compose_service']))


@roles('dev')
def deploy_development(rebuild, *args, **kwargs):
    print('deploy dev', env['host_string'])
    deploy_process(env.roledefs['dev'], rebuild)


@task
def deploy_dev(rebuild=False, *args, **kwargs):
    execute(deploy_development, rebuild)


@contextmanager
def project_context(role_config):
    with settings(sudo_prefix="sudo su {}".format(role_config['user'])), cd(role_config['project_path']):
        yield
