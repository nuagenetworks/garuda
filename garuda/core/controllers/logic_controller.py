# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('garuda.controller.logic')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.lib import ThreadManager

class GALogicController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """

        """
        super(GALogicController, self).__init__(plugins=plugins, core_controller=core_controller)

        self._managing_plugin_registry = []
        self._thread_manager = ThreadManager()

    def _managing_plugins(self, resource_name, action):
        """
        """
        key = "%s-%s" % (resource_name, action)

        if key in self._managing_plugin_registry:
            return self._managing_plugin_registry[key]

        for plugin in self._plugins:
            if plugin.should_manage(rest_name=resource_name, action=action):

                if not key in self._managing_plugin_registry:
                    self._managing_plugin_registry[key] = []

                self._managing_plugin_registry[key].append(plugin)

        return []

    def perform_delegate(self, delegate, context, timeout=2):
        """
        """
        jobs = []
        plugins = self._managing_plugins(resource_name=context.request.resources[-1].name, action=context.request.action)

        if not len(plugins):
            return

        for plugin in plugins:
            method = getattr(plugin, delegate, None)
            jobs.append(self._thread_manager.start(method, context=context.copy()))

        self._thread_manager.wait_until_exit()

        contexts = [job.value for job in jobs]

        context.merge_contexts(contexts)
