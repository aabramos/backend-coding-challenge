# !/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='backend_coding_challenge',
    author='Adriano Alberto Borges Ramos',
    version='1.0',
    packages=['app', 'unbabel'],
    include_package_data=True,
    install_requires=[
        'flask',
    ]
)
