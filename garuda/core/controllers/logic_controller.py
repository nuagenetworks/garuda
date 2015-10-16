# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('garuda.controller.logic')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.lib import ThreadManager
from garuda.core.plugins import GALogicPlugin

class GALogicController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """

        """
        super(GALogicController, self).__init__(plugins=plugins, core_controller=core_controller)

        self._managing_plugin_registry = {}
        self._thread_manager = ThreadManager()

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(GALogicController, self).register_plugin(plugin=plugin, plugin_type=GALogicPlugin)

    # Implementation

    def _managing_plugins(self, resource_name, action):
        """
        """
        key = "%s-%s" % (resource_name, action)

        if key in self._managing_plugin_registry:
            return self._managing_plugin_registry[key]

        self._managing_plugin_registry[key] = []

        for plugin in self._plugins:
            if plugin.should_manage(rest_name=resource_name, action=action):
                self._managing_plugin_registry[key].append(plugin)

        return self._managing_plugin_registry[key]

    def perform_delegate(self, delegate, context):
        """
        """
        jobs = []
        plugins = self._managing_plugins(resource_name=context.request.resources[-1].name, action=context.request.action)

        if not len(plugins):
            return

        result = self._thread_manager.start(self._perform_delegate,
                                               elements=plugins,
                                               delegate=delegate,
                                               context=context)

        logger.info("Merging contexts %s" % result)
        context.merge_contexts(result)

    def _perform_delegate(self, plugin, delegate, context):
        """
        """
        method = getattr(plugin, delegate, None)
        if not method:
            return context
        logger.info("Calling delegate %s of plugin %s " % (delegate, plugin))
        return method(context=context.copy())
