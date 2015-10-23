# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.controller.plugin')

from plugin import GAPlugin
from controller import GAController

class GAPluginController(GAController):
    """
    """
    def __init__(self, plugins, core_controller, redis_conn=None):
        """
        """
        super(GAPluginController, self).__init__(core_controller=core_controller, redis_conn=redis_conn)

        self._pending_plugins = plugins
        self._plugins = []

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        raise NotImplementedError("managed_plugin_type method must be implemented")

    def ready(self):
        """
        """
        for plugin in self._pending_plugins:
            self.register_plugin(plugin=plugin)

    def register_plugin(self, plugin):
        """
        """
        plugin_type = self.managed_plugin_type()

        if not isinstance(plugin, plugin_type):
            logger.error("'%s' cannot register '%s': not a valid '%s'." % (self.__class__.__name__, plugin.manifest().identifier, plugin_type.__name__))
            return

        if plugin in self._plugins:
            logger.warn("'%s' cannot register '%s': already registered." % (self.__class__.__name__, plugin.manifest().identifier))
            return

        plugin.will_register()
        plugin.core_controller = self.core_controller
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
        plugin.core_controller = None
        plugin.did_unregister()

        logger.debug("'%s': successfuly unregistered '%s'" % (self.__class__.__name__, plugin.manifest().identifier))

    def unregister_all_plugins(self):
        """
        """
        for plugin in self._plugins:
            self.unregister_plugin(plugin)
