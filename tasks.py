import os
from invoke import task

project_name = 'trequire'
exec_file = "{}.pex".format(project_name)
exec_dir = "bin"

@task
def clean(c):
    py_files = [
        'build',
        'dist',
        '__pycache__',
        '*.pyc',
        '*.egg-info',
        '*.whl',
        'bin/*'
    ]
    print("Cleaning up...")
    for file in py_files:
        c.run("rm -rf {}".format(file))

@task
def build(c, debian=False):
    if not os.path.isdir(exec_dir):
        os.makedirs(exec_dir)

    if debian:
        c.run("sudo apt-get update")
        c.run("sudo apt-get install -y libssl-dev")

    c.run("pip install pex wheel")
    c.run("pip wheel -w . .")
    c.run("pex --disable-cache --python-shebang='/usr/bin/python3' -f $PWD {0} -e {0}.main:cli -o {1}".format(project_name, exec_file))
    
    if os.path.isfile(exec_file):
        c.run("chmod 755 {}.pex".format(project_name))
        c.run("mv {0}.pex bin/{0}".format(project_name))
    else:
        print("{} exec file does not exists".format(exec_file))
    
@task
def upload(c, internal=False, external=False):
    # All option based on .pypirc file
    if internal:
        c.run("python setup.py sdist upload -r pypicloud")
    if external:
        c.run("python setup.py sdist upload -r pypi")
    