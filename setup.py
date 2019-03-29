from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='trequire',
    version='0.1.0',
    author='Marius Stanca',
    author_email=['me@marius.xyz'],
    url='https://github.com/wmariuss/trequire.git',
    license='MIT',
    description='Create backend resources for Terraform states',
    packages=['trequire'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    package_data={'': ['README.md']},
    install_requires=['click>=7.0',
                      'cerberus==1.2',
                      'pyyaml',
                      'boto3==1.9.122',
                      'termcolor==1.1.0'],
    extras_require={
        'click': ['click>=7.0']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Build Tools',
    ],
    entry_points='''
        [console_scripts]
        trequire=trequire.cli:cli
    '''
)