# -*- coding: utf-8 -*-

import gevent

from utils import Action, GAContext
from gaexceptions import InternalInconsistencyException

READ_OPERATIONS_METHODS = ['GET', 'HEAD', 'OPTIONS']
WRITE_OPERATIONS_METHODS = ['POST', 'PUT', 'DELETE']


class CoreController(object):
    """

    """
    def __init__(self, session, request):
        """
        """
        self.context = GAContext(session=session, request=request)

    def do_read_operation(self, *args, **kwargs):
        """

        """
        plugins = PluginsManager.plugins_for_context(context=self.context)

        self.context = PluginsManager.perform_delegate(delegate='begin_read_operation', context=self.context.copy(), plugins=plugins, *args, **kwargs)


        self.context = PluginsManager.perform_delegate(delegate='should_perform_read', context=self.context.copy(), plugins=plugins, *args, **kwargs)


        if len(self.context.disagreement_reasons) > 0:
            raise Exception('\n/!\ Plugin stopped in `should_perform_read` due to the following reasons:\n%s' % self.context.disagreement_reasons)

        self.context = PluginsManager.perform_delegate(delegate='preprocess_read', context=self.context.copy(), plugins=plugins, *args, **kwargs)

        ModelController.read()

        self.context = PluginsManager.perform_delegate(delegate='end_read_operation', context=self.context.copy(), plugins=plugins, *args, **kwargs)


class PluginsManager(object):
    """

    """
    timeout = 2
    _plugins = []

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

    @classmethod
    def plugins_for_context(cls, context):
        """

        """
        return [plugin for plugin in cls._plugins if plugin.is_listening(rest_name=context.session.resource.rest_name, action=context.session.action)]

    @classmethod
    def perform_delegate(cls, delegate, context, plugins, *args, **kwargs):
        """
        """
        jobs = [gevent.spawn(getattr(plugin, delegate), context=context.copy(), *args, **kwargs) for plugin in plugins]
        gevent.joinall(jobs, timeout=cls.timeout)

        context.merge_contexts([job.value for job in jobs])

        return context


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
