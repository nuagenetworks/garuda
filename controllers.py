# -*- coding: utf-8 -*-

import gevent

from time import sleep
from utils import GAContext
from channels import RESTCommunicationChannel

from collections import namedtuple
PluginContext = namedtuple('PluginContext', ['plugin', 'context'])

# READ_OPERATIONS_METHODS = ['GET', 'HEAD', 'OPTIONS']
# WRITE_OPERATIONS_METHODS = ['POST', 'PUT', 'DELETE']

from multiprocessing import Process


class ProcessManager(object):
    """ Multi process manager

    """
    def __init__(self):
        """ Initializes a ProcessManager

        """
        self._processes = list()

    def wait_until_exit(self):
        """ Wait until all process are finished.

        """
        [t.join() for t in self._processes]

        self._processes = list()

    def start(self, method, *args, **kwargs):
        """ Start a method in a separate process

            Args:
                method: the method to start in a separate process
                args: Accept args/kwargs arguments
        """
        process = Process(target=method, args=args, kwargs=kwargs)
        process.is_daemon = True
        process.start()
        self._processes.append(process)

    def is_running(self):
        """ Returns true if one process is running
        """

        for process in self._processes:
            if process.is_alive():
                return True

        return False

    def stop_all(self):
        """ Stop all current processes
        """
        for process in self._processes:
            process.terminate()

        self.wait_until_exit()


class CoreController(object):
    """

    """
    def __init__(self):
        """
        """
        self._channels = []
        self._process_manager = ProcessManager()

        flask2000 = RESTCommunicationChannel(controller=self, port=2000, debug=True, use_reloader=False)
        flask3000 = RESTCommunicationChannel(controller=self, port=3000, debug=True, use_reloader=False)

        self.register_channel(flask2000)
        self.register_channel(flask3000)

    def register_channel(self, channel):
        """
        """
        if channel not in self._channels:
            self._channels.append(channel)

    def unregister_channel(self, channel):
        """
        """
        if channel in self._channels:
            self._channels.remove(channel)

    def start(self):
        """
        """
        for channel in self._channels:
            self._process_manager.start(channel.start)

    def is_running(self):
        """
        """
        return self._process_manager.is_running()

    def stop(self, signal=None, frame=None):
        """
        """
        self._process_manager.stop_all()

        for channel in self._channels:
            channel.stop()

    def launch_operation(self, session, request):
        """
        """
        # TODO: Indicate what to do in the operation

        context = GAContext(session=session, request=request)
        manager = OperationsManager(context=context)
        manager.do_read_operation()

        # TODO: Create response from context

        return {'status':200, 'data':'ok'}


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
        print '** Let the police...Wait for it...'
        sleep(5)
        print '...do the job **'

    @classmethod
    def read(cls, *args, **kwargs):
        """

        """
        print '** Let the police...Wait for it...'
        sleep(5)
        print '...do the job **'
