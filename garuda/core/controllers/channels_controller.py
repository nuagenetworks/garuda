# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.controller.communicationchannels')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.channels import GAChannel
from garuda.core.lib import ThreadManager

class GAChannelsController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAChannelsController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._thread_manager = ThreadManager()

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(GAChannelsController, self).register_plugin(plugin=plugin, plugin_type=GAChannel)

    # Implementation

    def start(self):
        """
        """
        for channel in self._plugins:
            if channel.internal_thread_management():
                channel.start()
            else:
                self._thread_manager.start(channel.start)

    def stop(self):
        """
        """
        for channel in self._plugins:
            channel.stop()

        self._thread_manager.stop_all()
