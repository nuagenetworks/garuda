# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('ext.tdlauthenticationplugin')

from garuda.core.lib import SDKsManager
from garuda.core.plugins import GAPluginManifest
from garuda.core.plugins.abstracts import GAAuthenticationPlugin


class TDLAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='TDL Authentifation', version=1.0, identifier="garuda.plugins.tdl.authentication")

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
        root_rest_name = SDKsManager().get_sdk("current").SDKInfo.root_object_class().rest_name

        if request.resources[0].name != root_rest_name:
            return None

        root = self.core_controller.storage_controller.get(root_rest_name, '1')

        if request.parameters["username"] == root.user_name and request.parameters["password"] == root.password:
            root.api_key = session.uuid
            root.password = None
            return root

        return None

