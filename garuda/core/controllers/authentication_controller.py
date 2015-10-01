# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Garuda.AuthenticationController')

from garuda.core.plugins.abstracts import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin


class AuthenticationController(GAPluginController):
    """

    """
    def __init__(self, plugins):
        """
        """
        super(AuthenticationController, self).__init__(plugins=plugins)

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(AuthenticationController, self).register_plugin(plugin=plugin, plugin_type=GAAuthenticationPlugin)

    # Implementation

    def authenticate(self, request):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(request=request):
                return plugin.authenticate(request=request)

        return None
