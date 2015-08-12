# -*- coding: utf-8 -*-

from time import sleep

from vsdhelpers import VSDKFactory

from bambou.exceptions import BambouHTTPError
from bambou import NURESTModelController

from vspk.vsdk.v3_2 import NUVSDSession, NUEnterprise

MODE_GARUDA_ONLY = 0
MODE_VSPK_ONLY = 1
MODE_NORMAL = 2

MODE = MODE_NORMAL
SLEEP_TIME = 0

class ModelsController(object):
    """

    """
    __session = None

    @classmethod
    def _start_session_if_necessary(cls):
        """
        """
        if cls.__session is None:

            if MODE == MODE_VSPK_ONLY:
                cls._session = NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url='https://135.227.222.88:8443')
            else:
                vsdk = VSDKFactory.get_vsdk_package()
                cls._session = vsdk.NUVSDSession(username='csproot', password='csproot', enterprise='csp', api_url='https://135.227.222.88:8443')

            cls._session.start()

    @classmethod
    def get_objects(cls, parent, resource_name):
        """
        """
        if MODE == MODE_GARUDA_ONLY:
            sleep(SLEEP_TIME)
            return [object(),object(),object(),object(),object()]

        cls._start_session_if_necessary()


        if MODE == MODE_VSPK_ONLY:
            enterprise = NUEnterprise(id='b554017b-8f51-4a39-8139-08a3d7f01951')
            return enterprise.domains.get()

        fetcher = parent.fetcher_for_rest_name(resource_name)

        if fetcher is None:
            return None

        return fetcher.get()

    @classmethod
    def get_object(cls, resource_name, resource_value):
        """
        """
        if MODE == MODE_GARUDA_ONLY:
            sleep(SLEEP_TIME)
            return object()

        cls._start_session_if_necessary()

        klass = NURESTModelController.get_first_model(resource_name)
        obj = klass(id=resource_value)

        if obj is None:
            return None

        (obj, connection) = obj.fetch()

        if connection.response.status_code >= 300:
            return None

        return obj

    # @classmethod
    # def create_object(cls, resource_name):
    #     """
    #     """
    #     if MODE == MODE_GARUDA_ONLY:
    #         sleep(SLEEP_TIME)
    #         return object()
    #
    #     cls._start_session_if_necessary()
    #
    #     obj = VSDKFactory.get_instance(resource_name)
    #
    #     if obj is None:
    #         raise NotFoundException('Unknown %s object' % resource_name)
    #
    #     return obj
    #
    # @classmethod
    # def save_object(cls, object, parent=None):
    #     """
    #     """
    #     if MODE == MODE_GARUDA_ONLY:
    #         sleep(SLEEP_TIME)
    #         return object()
    #
    #     cls._start_session_if_necessary()
    #
    #     if object.id:
    #         try:
    #             object.save()
    #         except BambouHTTPError as error:
    #             response = error.connection.response
    #             raise NotFoundException('Could not save %s with ID %s. [%s] %s' % (object.rest_name, object.id, response.status_code, response.reason))
    #
    #     elif parent:
    #         try:
    #             parent.create_child(object)
    #         except BambouHTTPError as error:
    #             response = error.connection.response
    #             raise NotFoundException('Could not create %s in %s (%s) %s. [%s] %s' % (object.rest_name, parent.rest_name, parent.id, response.status_code, response.reason))
    #     else:
    #         raise Exception('Save object error')

    @classmethod
    def get_current_user(cls):
        """
        """
        if MODE == MODE_GARUDA_ONLY:
            sleep(SLEEP_TIME)
            return object()

        cls._start_session_if_necessary()

        return cls._session.user
