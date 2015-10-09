# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.communicationchannelscontroller')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GACommunicationChannel
from garuda.core.lib import ThreadManager

class GACommunicationChannelsController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GACommunicationChannelsController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._thread_manager = ThreadManager()

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(GACommunicationChannelsController, self).register_plugin(plugin=plugin, plugin_type=GACommunicationChannel)

    # Implementation

    def start(self):
        """
        """
        for channel in self._plugins:
            self._thread_manager.start(channel.start)

    def stop(self):
        """
        """
        for channel in self._plugins:
            channel.stop()

        self._thread_manager.stop_all()
