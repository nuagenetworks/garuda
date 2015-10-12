# -*- coding: utf-8 -*-

from garuda.core.models import GAPlugin

class GALogicPlugin(GAPlugin):
    """

    """

    def should_manage(self, rest_name, action=None):
        """

        """
        manifest = self.manifest()
        if rest_name not in manifest.subscriptions:
            return False

        if action and action in manifest.subscriptions[rest_name]:
            return True

        return False

    # Read plugins

    def begin_read_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        return context

    def check_perform_read(self, context, object):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        return context

    def preprocess_read(self, context, object):
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

    # ReadAll plugins

    def begin_readall_operation(self, context):
        """
        Called once at the very beginning of a Read Operation.
        """
        return context

    def check_perform_readall(self, context, object):
        """
        Asks a plugin if it agrees on performing the Read Operation. If it doesn’t it returns a disagreement reason object explaining why.
        If, after executing all Plugins delegates, one disagreement reason has been returned, the Read Operation stops.
        """
        return context

    def preprocess_readall(self, context, object):
        """
        Give the plugin a chance to modify the object that is about to be sent back to the client.
        All modifications will be merged after all Plugins preprocessing.
        """
        return context

    def end_readall_operation(self, context):
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

    def check_perform_write(self, context):
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
