# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.controller.plugin')

from garuda.core.models import GAPlugin
from garuda.core.channels import GAChannel


class GAPluginController(object):
    """
    """
    def __init__(self, plugins, core_controller):
        """
        """

        self._core_controller = core_controller
        self._plugins = []

        for plugin in plugins:
            self.register_plugin(plugin=plugin)

    @property
    def core_controller(self):
        """
        """
        return self._core_controller

    def register_plugin(self, plugin, plugin_type):
        """
        """
        if not isinstance(plugin, plugin_type):
            logger.error("'%s' cannot register '%s': not a valid '%s'." % (self.__class__.__name__, plugin.manifest().identifier, plugin_type.__name__))
            return

        if plugin in self._plugins:
            logger.warn("'%s' cannot register '%s': already registered." % (self.__class__.__name__, plugin.manifest().identifier))
            return

        plugin.core_controller = self.core_controller

        plugin.will_register()
        self._plugins.append(plugin)
        plugin.did_register()

        logger.debug("'%s': successfuly registered '%s'" % (self.__class__.__name__, plugin.manifest().identifier))

    def unregister_plugin(self, plugin):
        """
        """

        if not plugin in self._plugins:
            logger.warn("'%s' cannot unregister '%s': not registered." % (self.__class__.__name__, plugin.manifest().identifier))
            return

        plugin.will_unregister()
        self._plugins.remove(plugin)
        plugin.did_unregister()
        plugin.core_controller = None

        logger.debug("'%s': successfuly unregistered '%s'" % (self.__class__.__name__, plugin.manifest().identifier))

    def unregister_all_plugins(self):
        """
        """
        for plugin in self._plugins:
            self.unregister_plugin(plugin)
