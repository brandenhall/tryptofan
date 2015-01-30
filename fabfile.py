from fabric.api import lcd, env, task, run, cd, settings, prefix, put
from fabric.contrib.project import rsync_project
from fabric.operations import local as lrun
from unipath import Path

ACTIVATE = 'source {0}/bin/activate'
UPDATE_REQS = '{0} install -r {1}requirements/{2}.txt'
COLLECT_STATIC = 'collectstatic --noinput --settings {0}.settings.{1}'
SYNCDB = 'syncdb --settings {0}.settings.{1}'
MIGRATE = 'migrate --settings {0}.settings.{1}'


@task
def local():
    env.run = lrun
    env.cd = lcd
    env.name = 'local'
    env.hosts = ['localhost']
    env.path = Path(__file__).ancestor(1) + "/"
    env.project = 'theeyes'
    env.virtualenv = 'virtualenv -p python'
    env.environment = env.path + 'venv'
    env.python = 'python'
    env.pip = 'pip '


@task
def clubhouse():
    env.run = run
    env.cd = cd
    env.user = 'pi'
    env.name = 'production'
    env.hosts = ['tryptofan.local']
    env.path = '/srv/tryptofan/'
    env.project = 'tryptofan'
    env.virtualenv = 'virtualenv -p pypy'
    env.environment = env.path + 'venv'
    env.warn_only = True
    env.python = 'python'.format(env.path)
    env.pip = 'pip --no-cache-dir'.format(env.path)
    env.restart = ('sudo service tryptofan restart',)


@task
def bootstrap():
    upload()
    env.cd(env.path)
    env.run('rm -rf {0}'.format(env.environment))
    env.run('mkdir -p {0}'.format(env.environment))
    env.run('{0} {1} --no-site-packages'.format(
        env.virtualenv, env.environment))
    update_requirements()


@task
def upload():
    if 'localhost' not in env.hosts:
        extra_opts = '--omit-dir-times'
        put('requirements', env.path)
        rsync_project(remote_dir=env.path,
                      local_dir='webroot',
                      delete=True,
                      extra_opts=extra_opts,
                      exclude=('.DS_Store',))
        rsync_project(remote_dir=env.path,
                      local_dir='tryptofan',
                      delete=True,
                      extra_opts=extra_opts,
                      exclude=('.DS_Store',
                               'logs',
                               '__pycache__',
                               '*.pyc',
                               '*.pyo'))


@task
def update_requirements():
    with prefix(ACTIVATE.format(env.environment)):
        env.run(UPDATE_REQS.format(env.pip, env.path, env.name))


@task
def restart():
    with settings(warn_only=True):
        for cmd in env.restart:
            env.run(cmd)


@task
def deploy():
    upload()
    restart()
