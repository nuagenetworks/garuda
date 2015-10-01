# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('Garuda.GAPluginController')

from .plugin import GAPlugin


class GAPluginController(object):
    """
    """
    def __init__(self, plugins):
        """
        """

        self._plugins = []

        for plugin in plugins:
            self.register_plugin(plugin=plugin)

    def register_plugin(self, plugin, plugin_type):
        """
        """
        if not isinstance(plugin, plugin_type):
            logger.error("Plugin %s cannot be registered to %s" % (plugin, self))
            return

        if plugin in self._plugins or not isinstance(plugin, GAPlugin):
            logger.warn("Plugin %s is already registered in controller %s" % (plugin, self))
            return

        logger.info("Register plugin %s in controller %s" % (plugin, self))

        plugin.will_register()
        self._plugins.append(plugin)
        plugin.did_register()

    def unregister_plugin(self, plugin):
        """
        """

        if plugin not in self._plugins:
            logger.warn("No plugin %s registered in controller %s" % (plugin, self))
            return

        logger.info("Unregister plugin %s in controller %s" % (plugin, self))
        plugin.will_unregister()
        self._plugins.remove(plugin)
        plugin.did_unregister()
