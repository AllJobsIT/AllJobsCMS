from contextlib import contextmanager

from fabric.api import env, roles, execute
from fabric.context_managers import settings, cd
from fabric.decorators import task
from fabric.operations import run

env.roledefs = {
    "dev": {
        'hosts': ['157.90.183.254'],
        'branch': 'master',
        'user': 'deploy',
        'compose_file': './docker-compose.yml',
        'compose_service': '',
        'project_path': '/home/deploy/AllJobsCMS'
    },
}


def deploy_process(role_config, rebuild=''):
    with project_context(role_config):
        run(
            "git checkout -f && git checkout {branch} && git pull origin {branch}".format(branch=role_config['branch']))
        run('docker compose -f {} down 2>/dev/null'.format(role_config['compose_file']))
        run('docker compose -f {} up -d --build 2>/dev/null'.format(role_config['compose_file']))
        run('docker system prune -a -f')


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
