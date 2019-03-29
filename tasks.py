import os
from invoke import task

project_name = 'treq'


@task
def clean(c):
    py_files = [
        'build',
        'dist',
        '__pycache__',
        '*.pyc',
        '*.egg-info',
        '*.whl',
        'bin/*.pex'
    ]
    print("Cleaning up...")
    for file in py_files:
        c.run("rm -rf {}".format(file))

@task
def build(c):
    exec_file = "{}.pex".format(project_name)

    c.run("pip install pex wheel")
    c.run("pip wheel -w . .")
    c.run("pex --disable-cache --python-shebang='/usr/bin/python3' -f $PWD {0} -e {0}.main:cli -o {1}".format(project_name, exec_file))
    c.run("mkdir -p bin")
    
    if os.path.isfile(exec_file):
        c.run("mv {}.pex bin/".format(project_name))
    else:
        print("{} exec file does not exists".format(exec_file))
    
@task
def upload(c, internal=False, external=False):
    if internal:
        c.run("python setup.py sdist upload -r pypicloud")
    if external:
        c.run("python setup.py sdist upload -r pypi")
    