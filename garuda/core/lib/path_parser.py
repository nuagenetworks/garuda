# -*- coding: utf-8 -*-

import re

from collections import namedtuple
from .utils import VSDKTransform

GAResource = namedtuple('GAResource', ['name', 'value'])

RESOURCE_MAPPING = {'allalarms': 'alarms'}


class PathParser(object):
    """ Parse Path to retrieve resources and values information

    """
    def __init__(self):
        """
        """
        self._version = None
        self._resources = []

    @property
    def resources(self):
        """
        """
        return self._resources

    @property
    def version(self):
        """
        """
        return self._version

    def parse(self, path, url_prefix='nuage/api/'):
        """ Parse the path to retrieve information

            Args:
                path: the path such as /enterprises/3/domains

            Returs:
                Returns a list of GAResource.

            Example:
                [GAResource(name=u'enterprises', value=3), GAResource(name=u'domains', value=None)]

        """
        if len(path) == 0:
            return

        if path.startswith('/'):
            path = path[1:]

        if path.startswith(url_prefix):
            path = path[len(url_prefix):]

        index = path.find('/')

        if index > 0 and re.match('v[0-9]_[0-9]', path[:index]):
            self._version = path[:index]
            path = path[index + 1:]

        infos = path.split('/')

        result = list()
        index = 0

        while index < len(infos):
            resource = infos[index]

            if resource and len(resource) > 0:

                index = index + 1
                value = infos[index] if index < len(infos) and len(infos[index]) > 0 else None

                name = self._get_resource(resource)
                result.append(GAResource(VSDKTransform.get_singular_name(name), value))

            index = index + 1

        self._resources = result
        return self._resources

    def _get_resource(cls, resource):
        """ Get the resource

        """
        if resource in RESOURCE_MAPPING:
            return RESOURCE_MAPPING[resource]

        return resource
