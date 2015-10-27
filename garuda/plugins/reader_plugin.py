# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.plugins.reader')

from garuda.core.models import GAError, GAPluginManifest
from garuda.core.plugins import GALogicPlugin

from time import sleep

class ReaderPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='Reader Plugin',
                                version=1.0,
                                identifier="garuda.plugins.test.reader",
                                subscriptions={
                                                "subnet": ["READ_ALL", "DELETE"],
                                                "subnettemplate": ["READALL", "UPDATE"],
                                                "list": ["READ_ALL"]
                                              })

    def begin_readall_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        logger.info('ReaderPlugin\t\tbegin_readall_operation\t\t(Host=%s)' % context.request.parameters['Host'])

        return context

    def check_perform_readall(self, context):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        logger.info('ReaderPlugin\t\tcheck_perform_readall\t\t(Host=%s)' % context.request.parameters['Host'])
        # context.add_error(type=GAError.TYPE_INVALID, property='name', title='name is too long', description='name should have maximum 255 characters')
        return context

    def preprocess_readall(self, context):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        logger.info('ReaderPlugin\t\tpreprocess_readall\t\t(Host=%s)' % context.request.parameters['Host'])
        return context

    def end_readall_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        logger.info('ReaderPlugin\t\tend_readall_operation\t\t(Host=%s)' % context.request.parameters['Host'])
        return context
