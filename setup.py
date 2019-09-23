from setuptools import setup

setup(
    name="trequire",
    version="0.3.0",
    author="Marius Stanca",
    author_email=["me@marius.xyz"],
    url="https://github.com/wmariuss/trequire.git",
    license="MIT",
    description="Create backend resources for Terraform states",
    packages=["trequire"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={"": ["README.md"]},
    install_requires=[
        "click>=7.0",
        "cerberus==1.2",
        "pyyaml",
        "boto3==1.9.122",
        "botocore==1.12.127",
        "termcolor==1.1.0",
    ],
    extras_require={"click": ["click>=7.0"]},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Build Tools",
    ],
    entry_points="""
        [console_scripts]
        trequire=trequire.main:cli
    """,
)
