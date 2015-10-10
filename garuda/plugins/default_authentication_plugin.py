# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('ext.defaultauthenticationplugin')

from garuda.core.lib import SDKLibrary
from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAAuthenticationPlugin


class DefaultAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='VSD Authentifcation',
                                version=1.0,
                                identifier="garuda.plugins.vsd.authentication")

    def should_manage(self, request):
        """
        """
        return True

    def authenticate(self, request):
        """
        """

        if 'username' not in request.parameters or \
           'password' not in request.parameters or \
           'X-Nuage-Organization' not in request.parameters:
           logger.debug("No information provided to authenticate user")
           return None

        username = request.parameters['username']
        password = request.parameters['password']
        enterprise = request.parameters['X-Nuage-Organization']

        logger.debug("Authenticate user with username=%s, password=%s, enterprise=%s" % (username, password, enterprise))

        sdk_library = SDKLibrary()
        sdk_session_class = sdk_library.get_sdk_session_class('vspk32')
        session = sdk_session_class(username=username, password=password, enterprise=enterprise, api_url="put that as a parameter")
        session.start()

        return session.user

