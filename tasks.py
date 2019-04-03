import os
from invoke import task

project_name = 'trequire'


@task
def clean(c):
    files = [
        'build',
        'dist',
        '__pycache__',
        '*.pyc',
        '*.egg-info',
        '*.whl',
        '*.pex'
    ]
    print('Cleaning up...')
    for f in files:
        c.run('rm -rf {}'.format(f))
    
@task
def upload(c, internal=False, external=False):
    '''All option based on .pypirc file
    '''
    if internal:
        c.run('python setup.py sdist upload -r pypicloud')
    if external:
        c.run('python setup.py sdist upload -r pypi')
    