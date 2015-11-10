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

    # Read Operations

    def will_perform_read(self, context):
        """
        """
        return context

    def did_perform_read(self, context):
        """
        """
        return context

    # ReadAll Operations

    def will_perform_readall(self, context):
        """
        """
        return context

    def did_perform_readall(self, context):
        """
        """
        return context

    # General Write operations

    def will_perform_write(self, context):
        """
        """
        return context

    def did_perform_write(self, context):
        """
        """
        return context

    # Create operations

    def will_perform_create(self, context):
        """
        """
        return context

    def did_perform_create(self, context):
        """
        """
        return context

    # Update operations

    def will_perform_update(self, context):
        """
        """
        return context

    def did_perform_update(self, context):
        """
        """
        return context

    # Delete operations

    def will_perform_delete(self, context):
        """
        """
        return context

    def did_perform_delete(self, context):
        """
        """
        return context

    # Assign operations

    def will_perform_assign(self, context):
        """
        """
        return context

    def did_perform_assign(self, context):
        """
        """
        return context
