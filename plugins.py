# -*- coding: utf-8 -*-


class PluginManifest(object):

    def __init__(self, name, subscriptions):
        """

        """
        self.name = name
        self.subscriptions = subscriptions


class AbstractPlugin(object):
    """

    """
    @property
    def manifest(self):
        """

        """
        raise NotImplementedException('Plugin should implement its manifest method')


    def is_listening(self, rest_name, action=None):
        """

        """
        if self.manifest is None:
            return False

        if rest_name not in self.manifest.subscriptions:
            return False

        if action and action in self.manifest.subscriptions[rest_name]:
            return True

        return False

    # Read plugins

    def begin_read_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        return context

    def should_perform_read(self, context):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        return context

    def preprocess_read(self, context):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        return context

    def end_read_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        return context

    # Write plugins

    def begin_write_operation(self, context):
        """
        Called once at the very beginning of a Write Operation.
        """
        return context

    def should_perform_write(self, context):
        """
        Asks if a plugin agrees on performing the Write Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If after executing all Plugins delegates, one disagreement reason has been returned, the Write Operation stops.
        """
        return context

    def preprocess_write(self, context):
        """
        Give the plugin a chance to modify the object that is about to be written into the Database.
        All modifications will be merged after all Plugins preprocessing.
        """
        return context

    def did_perform_write(self, context):
        """
        Called after the modification of the object has been written into the Database.
        """
        return context

    def end_write_operation(self, context):
        """
        Called once at the very end of a Write Operation
        """
        return context


class ReaderPlugin(AbstractPlugin):
    """

    """
    @property
    def manifest(self):
        """

        """

        return PluginManifest(name='Reader Plugin', subscriptions={"subnets": ["readall", "delete"], \
                                                                   "subnettemplates": ["readall", "update"]})

    def begin_read_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        print 'ReaderPlugin\t\tbegin_read_operation\t\t(Host=%s)' % context.request.headers['Host']

        return context

    def should_perform_read(self, context):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        print 'ReaderPlugin\t\tshould_perform_read\t\t(Host=%s)' % context.request.headers['Host']
        context.report_error(property='name', title='name is too long', description='name should have maximum 255 characters')
        return context

    def preprocess_read(self, context):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        print 'ReaderPlugin\t\tpreprocess_read\t\t(Host=%s)' % context.request.headers['Host']
        return context

    def end_read_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        print 'ReaderPlugin\t\tend_read_operation\t\t(Host=%s)' % context.request.headers['Host']
        return context


class AnotherPlugin(AbstractPlugin):
    """

    """
    @property
    def manifest(self):
        """

        """

        return PluginManifest(name='Another Plugin', subscriptions={"subnets": ["readall", "delete"], \
                                                                    "domains": ["readall", "update"]})

    def begin_read_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        print 'AnotherPlugin\t\tbegin_read_operation\t\t(Host=%s)' % context.request.headers['Host']

        return context

    def should_perform_read(self, context):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        print 'AnotherPlugin\t\tshould_perform_read\t\t(Host=%s)' % context.request.headers['Host']
        return context

    def preprocess_read(self, context):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        print 'AnotherPlugin\t\tpreprocess_read\t\t(Host=%s)' % context.request.headers['Host']
        return context

    def end_read_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        print 'AnotherPlugin\t\tend_read_operation\t\t(Host=%s)' % context.request.headers['Host']
        return context
