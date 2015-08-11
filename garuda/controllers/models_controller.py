# -*- coding: utf-8 -*-

from time import sleep

from vsdhelpers import VSDKFactory

from garuda.exceptions import NotFoundException

from bambou.exceptions import BambouHTTPError


DEBUG = True
SLEEP_TIME = 0

class ModelsController(object):
    """

    """
    def __init__(self, username='csproot', password='csproot', enterprise='csp', api_url='https://135.227.222.88:8443'):
        """
        """
        if not DEBUG:
            vsdk = VSDKFactory.get_vsdk_package()
            self._session = vsdk.NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=api_url)
            self._session.start()

    def get_objects(self, parent, resource_name):
        """
        """
        if DEBUG:
            sleep(SLEEP_TIME)
            return [object(),object(),object(),object(),object()]

        fetcher = VSDKFactory.get_fetcher(parent, resource_name)

        if fetcher is None:
            raise NotFoundException('Unknown %s objects' % resource_name)

        return fetcher.get()

    def get_object(self, resource_name, resource_value):
        """
        """
        if DEBUG:
            sleep(SLEEP_TIME)
            return object()

        obj = VSDKFactory.get_instance(resource_name, id=resource_value)

        if obj is None:
            raise NotFoundException('Unknown %s object' % resource_name)

        try:
            (obj, connection) = obj.fetch()
        except BambouHTTPError as error:
            response = error.connection.response
            raise NotFoundException('Could not retrieve %s object. [%s] %s' % (resource_name, response.status_code, response.reason))

        return obj

    def create_object(self, resource_name):
        """
        """
        if DEBUG:
            sleep(SLEEP_TIME)
            return object()

        obj = VSDKFactory.get_instance(resource_name)

        if obj is None:
            raise NotFoundException('Unknown %s object' % resource_name)

        return obj

    def save_object(self, object, parent=None):
        """
        """
        if DEBUG:
            sleep(SLEEP_TIME)
            return object()

        if object.id:
            try:
                object.save()
            except BambouHTTPError as error:
                response = error.connection.response
                raise NotFoundException('Could not save %s with ID %s. [%s] %s' % (object.rest_name, object.id, response.status_code, response.reason))

        elif parent:
            try:
                parent.create_child(object)
            except BambouHTTPError as error:
                response = error.connection.response
                raise NotFoundException('Could not create %s in %s (%s) %s. [%s] %s' % (object.rest_name, parent.rest_name, parent.id, response.status_code, response.reason))
        else:
            raise Exception('Save object error')

    def get_current_user(self):
        """
        """
        if DEBUG:
            sleep(SLEEP_TIME)
            return object()

        return self._session.user
