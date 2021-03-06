# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.plugin.authentication.simple')

from garuda.core.lib import GASDKLibrary
from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAAuthenticationPlugin


class GASimpleAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    def __init__(self, auth_function=None):
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

    def extract_session_identifier(self, request):
        """
        """
        return request.token

    def authenticate(self, request, session):
        """
        """
        root_object_class = GASDKLibrary().get_sdk('default').SDKInfo.root_object_class()
        root_api = root_object_class.rest_name

        if request.resources[0].name != root_api:
            return None

        if self._auth_function:
            return self._auth_function(request=request, session=session, root_object_class=root_object_class, storage_controller=self.core_controller.storage_controller)
        else:
            auth = root_object_class()
            auth.api_key = session.uuid
            auth.password = None
            return auth
