# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('ext.defaultgamodelcontrollerplugin')

from bambou import NURESTModelController
from bambou.nurest_session import _NURESTSessionCurrentContext
from garuda.core.config import GAConfig
from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAStoragePlugin
from garuda.core.lib import SDKLibrary


class DefaultGAStoragePlugin(GAStoragePlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='VSD Model Controller',
                                version=1.0,
                                identifier="garuda.plugins.vsd.modelcontroller")

    def __init__(self):
        """
        """
        super(DefaultGAStoragePlugin, self).__init__()

        self._sdk_session = None

    def _use_session(self):
        """
        """
        if self._sdk_session is None:
            sdk_library = SDKLibrary()
            session_class = sdk_library.get_sdk_session_class('vspk32')

            if session_class:
                self._sdk_session = session_class(username=GAConfig.VSD_USERNAME, password=GAConfig.VSD_PASSWORD, enterprise=GAConfig.VSD_ENTERPRISE, api_url=GAConfig.VSD_API_URL)
                self._sdk_session.start()
                logger.debug('Started SDK Session with user %s' % self._sdk_session.user.user_name)


        _NURESTSessionCurrentContext.session = self._sdk_session

    def _get_current_user(self):
        """
        """
        self._use_session()
        return self._sdk_session.user

    # Implementation

    def should_manage(self, resource_name, identifier):
        """
        """
        return True

    def instantiate(self, resource_name):
        """
        """
        self._use_session()

        logger.debug('Create object %s' % resource_name)

        klass = NURESTModelController.get_first_model(resource_name)
        obj = klass()

        # TODO: Uncomment this line once validation is working
        # obj.validate()
        return obj

    def get_all(self, parent, resource_name):
        """
        """

        if parent is None:
            parent = self._get_current_user()

        logger.debug('Get objects %s with parent=%s' % (resource_name, parent))
        fetcher = parent.fetcher_for_rest_name(resource_name)

        if fetcher is None:
            return None

        return fetcher.get()

    def get(self, resource_name, identifier):
        """
        """
        self._use_session()

        logger.debug('Get object %s with ID=%s' % (resource_name, identifier))

        klass = NURESTModelController.get_first_model(resource_name)
        obj = klass(id=identifier)

        if obj is None:
            return None

        (_, connection) = obj.fetch()

        if connection.response.status_code >= 300:
            return None

        return obj

    def save(self, resource, parent=None):
        """
        """
        self._use_session()

        # TODO: Uncomment this line once validation is working
        # resource.validate()

        if len(resource.errors) > 0:
            return False

        if resource.id:
            logger.debug('Save object %s' % resource)

            (resource, connection) = resource.save()

            if connection.response.status_code >= 300:
                return False  # TODO: This is temporarely bad

            return resource

        if parent is None:
            parent = self._get_current_user()

        logger.debug('Save object %s with parent=%s' % (resource, parent))

        (resource, connection) = parent.create_child(resource)

        if connection.response.status_code >= 300:
            return False  # TODO: This is temporarely bad

        return resource

    def delete(self, resource):
        """
        """
        self._use_session()

        logger.debug('Delete object %s with ID=%s' % (resource, resource.id))

        resource.delete()
