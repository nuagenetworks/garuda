# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Garuda.GAAuthenticationController')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAAuthenticationPlugin


class GAAuthenticationController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAAuthenticationController, self).__init__(plugins=plugins, core_controller=core_controller)

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(GAAuthenticationController, self).register_plugin(plugin=plugin, plugin_type=GAAuthenticationPlugin)

    # Implementation

    def authenticate(self, request):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(request=request):
                return plugin.authenticate(request=request)

        return None
