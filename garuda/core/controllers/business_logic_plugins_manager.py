# -*- coding: utf-8 -*-

import gevent
import logging

logger = logging.getLogger('Garuda.GABusinessLogicPluginsManager')

from garuda.core.exceptions import InternalInconsistencyException
from collections import namedtuple
PluginContext = namedtuple('PluginContext', ['plugin', 'context'])


class GABusinessLogicPluginsManager(object):
    """

    """
    _plugins = []

    def __init__(self, context, timeout=2):
        """

        """
        self.context = context  # Plugin contexts' parent
        self.timeout = timeout  # Gevent spawn timeout
        self.plugins_contexts = []  # Plugins available for the current context

        resource_name = context.request.resources[-1].name

        for plugin in self._plugins:
            if plugin.is_listening(rest_name=resource_name, action=context.request.action):
                plugin_context = PluginContext(plugin=plugin, context=context.copy())
                self.plugins_contexts.append(plugin_context)

    @classmethod
    def register_plugin(cls, plugin):
        """
        """
        cls._plugins.append(plugin)

    @classmethod
    def unregister_plugin(cls, plugin):
        """
        """
        cls._plugins.remove(plugin)

    def perform_delegate(self, delegate, *args, **kwargs):
        """
        """
        if len(self.plugins_contexts) == 0:
            return

        jobs = []
        for plugin_context in self.plugins_contexts:

            plugin = plugin_context.plugin
            context = plugin_context.context
            method = getattr(plugin, delegate, None)

            if method:
                jobs.append(gevent.spawn(method, context=context, *args, **kwargs))
            else:
                raise InternalInconsistencyException("%s does not have delegate method %s " % (plugin, delegate))

        gevent.joinall(jobs, timeout=self.timeout)

        contexts = [job.value for job in jobs]
        self.context.merge_contexts(contexts)
