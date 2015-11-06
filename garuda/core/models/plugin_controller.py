# -*- coding: utf-8 -*-

import logging
import copy

from controller import GAController

logger = logging.getLogger('garuda.controller.plugin')


class GAPluginController(GAController):
    """
    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAPluginController, self).__init__(core_controller=core_controller)

        self._pending_plugins = plugins
        self._plugins = []

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        raise NotImplementedError("managed_plugin_type method must be implemented")

    @property
    def plugins(self):
        return self._plugins

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
            raise AssertionError("'%s' cannot register '%s': not a valid '%s'." % (self.__class__.__name__, plugin.manifest().identifier, plugin_type.__name__))

        if plugin in self._plugins:
            raise AssertionError("'%s' cannot register '%s': already registered." % (self.__class__.__name__, plugin.manifest().identifier))

        plugin.will_register()
        plugin.core_controller = self.core_controller
        self._plugins.append(plugin)
        plugin.did_register()

        logger.debug("'%s': successfuly registered '%s'" % (self.__class__.__name__, plugin.manifest().identifier))

    def unregister_plugin(self, plugin):
        """
        """
        if plugin not in self._plugins:
            raise AssertionError("'%s' cannot unregister '%s': not registered." % (self.__class__.__name__, plugin.manifest().identifier))

        plugin.will_unregister()
        self._plugins.remove(plugin)
        plugin.core_controller = None
        plugin.did_unregister()

        logger.debug("'%s': successfuly unregistered '%s'" % (self.__class__.__name__, plugin.manifest().identifier))

    def unregister_all_plugins(self):
        """
        """
        plugins = copy.copy(self._plugins)

        for plugin in plugins:
            self.unregister_plugin(plugin)
