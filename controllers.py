# -*- coding: utf-8 -*-

import gevent

from utils import GAContext
from gaexceptions import InternalInconsistencyException

from collections import namedtuple
PluginContext = namedtuple('PluginContext', ['plugin', 'context'])

# READ_OPERATIONS_METHODS = ['GET', 'HEAD', 'OPTIONS']
# WRITE_OPERATIONS_METHODS = ['POST', 'PUT', 'DELETE']


class CoreController(object):
    """

    """
    def __init__(self, session, request):
        """
        """
        self.context = GAContext(session=session, request=request)

class OperationsManager(object):
    """

    """
    def __init__(self, context):
        """
        """
        self.context = context

    def do_read_operation(self, *args, **kwargs):
        """

        """
        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_read_operation', *args, **kwargs)

        plugin_manager.perform_delegate(delegate='should_perform_read', *args, **kwargs)

        if len(self.context.disagreement_reasons) > 0:
            raise Exception('\n/!\ Plugin stopped in `should_perform_read` due to the following reasons:\n%s' % self.context.disagreement_reasons)

        plugin_manager.perform_delegate(delegate='preprocess_read', *args, **kwargs)

        ModelController.read()

        plugin_manager.perform_delegate(delegate='end_read_operation', *args, **kwargs)


class PluginsManager(object):
    """

    """
    _plugins = []

    def __init__(self, context, timeout=2):
        """

        """
        self.context = context  # Plugin contexts' parent
        self.timeout = timeout  # Gevent spawn timeout
        self.plugins_contexts = []  # Plugins available for the current context

        for plugin in self._plugins:
            if plugin.is_listening(rest_name=context.session.resource.rest_name, action=context.session.action):
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

        gevent.joinall(jobs, timeout=self.timeout)

        self.context.merge_contexts([job.value for job in jobs])


class ModelController(object):
    """

    """
    @classmethod
    def write(cls, *args, **kwargs):
        """

        """
        print '** Let the police write the job **'

    @classmethod
    def read(cls, *args, **kwargs):
        """

        """
        print '** Let the police read the job **'
