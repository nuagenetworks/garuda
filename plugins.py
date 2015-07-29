# -*- coding: utf-8 -*-

import json

from utils import DisagreementReason


class PluginManifest(object):

    def __init__(self, filepath):
        """

        """
        self.from_manifest(filepath)

    @classmethod
    def from_manifest(self, filepath):
        """

        """
        f = open(filepath, 'r')
        data = json.loads(f.read())
        f.close()

        self.name = data['information']['name']
        self.identifier = data['information']['identifier']
        self.version = data['information']['version']
        self.author = data['information']['author']

        self.subscriptions = data['subscriptions']

class AbstractPlugin(object):
    """

    """
    def __init__(self, filepath='manifest.json'):
        """

        """
        self._manifest = PluginManifest(filepath)

    def is_listening(self, rest_name, action=None):
        """

        """
        if self._manifest is None:
            return False

        if rest_name not in self._manifest.subscriptions:
            return False

        if action and action in self._manifest.subscriptions[rest_name]:
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

    def begin_read_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        print 'ReaderPlugin begin_read_operation'

        return context

    def should_perform_read(self, context):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        print 'ReaderPlugin should_perform_read'
        # context.disagreement_reasons.append(DisagreementReason(origin=self, reason='Something wrong happened', suggestion='Try again after 120s... just kidding'))
        return context

    def preprocess_read(self, context):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        print 'ReaderPlugin preprocess_read'
        return context

    def end_read_operation(self, context):
        """
        Called once at the very end of a Read Operation
        """
        print 'ReaderPlugin end_read_operation'
        return context
