# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('ext.tdlauthenticationplugin')

from garuda.core.lib import SDKsManager
from garuda.core.plugins import GAAuthenticationPlugin, GAPluginManifest
from garuda.core.config import GAConfig


class TDLAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='TDL Authentifcation', version=1.0, identifier="garuda.plugins.vsd.authentication")

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
        root = self.core_controller.model_controller.get('root', 'root-id-1')

        if request.parameters["username"] == root.user_name and request.parameters["password"] == root.password:
            root.api_key = session.uuid
            root.password = None
            return root

        return None

