# -*- coding:utf-8 -*-

import os
from setuptools  import setup

setup(
    name='garuda',
    version='0.0.1',
    author='Christophe Serafin',
    packages=['garuda', 'garuda.core', 'garuda.plugins', 'garuda.channels'],
    author_email='christophe.serafin@nuagenetworks.net, antoine@nuagenetworks.net',
    description='Garuda is the future. No more. No less.',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
    license='TODO',
    url='TODO'
)
