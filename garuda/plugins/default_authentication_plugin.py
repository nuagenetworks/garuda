# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('Garuda.plugins.DefaultAuthenticationPlugin')

from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.config import GAConfig
from garuda.core.lib.utils import VSDKLoader


class DefaultAuthenticationPlugin(GAAuthenticationPlugin):
    """
    """

    def __init__(self):
        """
        """
        self._vsdk = VSDKLoader.get_vsdk_package(version=3.2)  # TODO: Later this should be in a configuration file
        self._vsd_session = self._vsdk.NUVSDSession(username=GAConfig.VSD_USERNAME, password=GAConfig.VSD_PASSWORD, enterprise=GAConfig.VSD_ENTERPRISE, api_url=GAConfig.VSD_API_URL)
        self._vsd_session.start()
        logger.debug('Started VSD Session with user %s' % self._vsd_session.user.user_name)

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

        session = self._vsdk.NUVSDSession(username=username, password=password, enterprise=enterprise, api_url=GAConfig.VSD_API_URL)
        session.start()

        return session.user
