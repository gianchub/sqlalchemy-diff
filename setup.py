#!/usr/bin/env python
from codecs import open
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as stream:
    readme = stream.read()


setup(
    name='sqlalchemy-diff',
    version='0.1.2',
    description='Compare two database schemas using sqlalchemy.',
    long_description=readme,
    author='student.com',
    author_email='wearehiring@student.com',
    url='https://github.com/Overseas-Student-Living/sqlalchemy-diff',
    packages=find_packages(exclude=['docs', 'test', 'test.*']),
    install_requires=[
        "six>=1.10.0",
        "sqlalchemy-utils>=0.32.4",
    ],
    extras_require={
        'dev': [
            "mock==2.0.0",
            "mysql-connector-python==2.0.4",
            "pytest==3.0.3",
            "flake8==3.0.4",
            "coverage==4.2",
        ],
        'docs': [
            "sphinx==1.4.1",
        ],
    },
    zip_safe=True,
    license='Apache License, Version 2.0',
    classifiers=[
        "Programming Language :: Python",
        "Operating System :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ]
)
