# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README') as f:
    readme = f.read()


with open('LICENSE') as f:
    license = f.read()


setup(
    name='sample',
    version='0.1.0',
    description='A structural solver written in python',
    long_description=readme,
    author='Nicolo Bencini',
    author_email='nicbencini@gmail.com',
    url='https://github.com/nicbencini/PyDr_Solver',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
    
)