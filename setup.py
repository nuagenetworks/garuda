# -*- coding:utf-8 -*-

import os
from setuptools  import setup

setup(
    name='garuda',
    version='0.0.1',
    author='Christophe Serafin',
    packages=['garuda', 'channels', 'plugins'],
    author_email='christophe.serafin@nuagenetworks.net',
    description='Garuda is the future. No more. No less.',
    long_description=open('README.md').read(),
    install_requires=[line for line in open('requirements.txt')],
    license='TODO',
    url='TODO',
    entry_points={
        'console_scripts': [
            'garuda = garuda:main']
    },
)
