# -*- coding:utf-8 -*-

import os
from setuptools  import setup
import pip

setup(
    name='garuda',
    version='0.0.1',
    author='Christophe Serafin',
    packages=[  'garuda',
                'garuda.plugins',
                'garuda.plugins.authentication',
                'garuda.plugins.storage',
                'garuda.channels',
                'garuda.channels.rest',
                'garuda.core',
                'garuda.core.channels',
                'garuda.core.controllers',
                'garuda.core.lib',
                'garuda.core.models',
                'garuda.core.plugins'],

    author_email='christophe.serafin@nuagenetworks.net, antoine@nuagenetworks.net',
    description='Garuda is the future. No more. No less.',
    long_description=open('README.md').read(),
    install_requires=[str(ir.req) for ir in pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())],
    license='TODO',
    url='TODO'
)
