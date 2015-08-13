# -*- coding: utf-8 -*-

from garuda.models.abstracts import PluginManifest, GAPlugin


class AnotherPlugin(GAPlugin):
    """

    """
    @property
    def manifest(self):
        """

        """

        return PluginManifest(name='Another Plugin', subscriptions={"subnet": ["readall", "delete"], \
                                                                    "domain": ["readall", "update"]})

    def begin_readall_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        print 'AnotherPlugin\t\tbegin_read_operation\t\t(Host=%s)' % context.request.parameters['Host']

        return context

    def should_perform_readall(self, context, object):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        print 'AnotherPlugin\t\tshould_perform_read\t\t(Host=%s)' % context.request.parameters['Host']
        return context

    def preprocess_readall(self, context, object):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        print 'AnotherPlugin\t\tpreprocess_read\t\t(Host=%s)' % context.request.parameters['Host']
        return context

    def end_readall_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        print 'AnotherPlugin\t\tend_read_operation\t\t(Host=%s)' % context.request.parameters['Host']
        return context
