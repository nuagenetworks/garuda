# -*- coding: utf-8 -*-

from collections import namedtuple

GAResource = namedtuple('GAResource', ['name', 'value'])

RESOURCE_MAPPING = {
    'allalarms': 'alarms'
}


class PathParser(object):
    """ Parse Path to retrieve resources and values information

    """
    def parse(self, path):
        """ Parse the path to retrieve information

            Args:
                path: the path such as /enterprises/3/domains

            Returs:
                Returns a list of GAResource.

            Example:
                [GAResource(name=u'enterprises', value=3), GAResource(name=u'domains', value=None)]

        """
        if path.startswith('/'):
            path = path[1:]

        infos = path.split('/')

        result = list()
        index = 0

        while index < len(infos):
            resource = infos[index]

            if resource and len(resource) > 0:

                index = index + 1
                value = infos[index] if index < len(infos) and len(infos[index]) > 0 else None
                result.append(GAResource(self._get_resource(resource), value))

            index = index + 1

        return result

    def _get_resource(cls, resource):
        """ Get the resource

        """
        if resource in RESOURCE_MAPPING:
            return RESOURCE_MAPPING[resource]

        return resource