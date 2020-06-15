# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Python-Wtachlist-Generator',
    version='0.2.0',
    description='python watchlist generator',
    long_description=readme,
    author='Nathan Kroyzer',
    author_email='kroizer21@gmail.com',
    url='https://github.com/Nkroizer/Python-Wtachlist-Generator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
