# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.plugin.authentication.simple')

from garuda.core.lib import SDKsManager
from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAAuthenticationPlugin


class GASimpleAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    def __init__(self, auth_function):
        """
        """
        super(GASimpleAuthenticationPlugin, self).__init__()

        self._auth_function = auth_function

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='simple', version=1.0, identifier='garuda.plugin.authentication.simple')

    def should_manage(self, request):
        """
        """
        return True

    def get_session_identifier(self, request):
        """
        """
        return request.parameters['password']

    def authenticate(self, request, session):
        """
        """
        root_api = SDKsManager().get_sdk('default').SDKInfo.root_object_class().rest_name

        if request.resources[0].name != root_api:
            return None

        return self._auth_function(request=request, session=session, root_api=root_api, storage_controller=self.core_controller.storage_controller)