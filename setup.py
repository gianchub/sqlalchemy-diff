#!/usr/bin/env python
from codecs import open
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as stream:
    readme = stream.read()


setup(
    name='sqlalchemy-diff',
    version='0.0.1',
    description='Compare two database schemas using sqlalchemy.',
    long_description=readme,
    author='student.com',
    author_email='dark-side@student.com',  # TODO - Add proper email here
    url='https://github.com/Overseas-Student-Living/sqlalchemy-diff',
    packages=find_packages(exclude=['docs', 'test', 'test.*']),
    install_requires=[
        "six==1.10.0",
        "mock==1.3.0",
        "mysql-connector-python==2.0.4",
        "sqlalchemy-utils==0.31.2",
    ],
    extras_require={
        'dev': [
            "pytest==2.8.2",
        ],
        'docs': [
            "Sphinx==1.3.1",
        ],
    },
    entry_points={
        'pytest11': [
            'sqlalchemy_diff=sqlalchemydiff.pyfixtures'
        ]
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
