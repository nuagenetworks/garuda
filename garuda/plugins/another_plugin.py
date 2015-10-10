# -*- coding: utf-8 -*-

from garuda.core.models import GAError
from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GABusinessLogicPlugin


class AnotherPlugin(GABusinessLogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """

        return GAPluginManifest(name='Another Plugin',
                                version=1.0,
                                identifier="garuda.plugins.test.another",
                                subscriptions={"subnet": ["readall", "delete"], "domain": ["readall", "update"]})

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
        # context.report_error(type=GAError.TYPE_INVALID, property='what', title='NOWAY', description='TUUTUTUTUUT')
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
