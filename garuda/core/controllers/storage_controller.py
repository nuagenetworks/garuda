# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.controller.storage')

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAStoragePlugin


class GAStorageController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAStorageController, self).__init__(plugins=plugins, core_controller=core_controller)
        self._managing_plugin_registry = {}

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.storage'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAStoragePlugin

    # Override

    def unregister_plugin(self, plugin):
        """
        """
        super(GAStorageController, self).unregister_plugin(plugin=plugin)

        keys_to_remove = []
        for resource_name, plugin in self._managing_plugin_registry.iteritems():
            if self._managing_plugin_registry[resource_name] == plugin:
                keys_to_remove.append(resource_name)

        for key in keys_to_remove:
            del self._managing_plugin_registry[key]

    # Implementation

    def instantiate(self, resource_name):
        """
        """
        plugin = self._managing_plugin(resource_name=resource_name, identifier=None)
        return plugin.instantiate(resource_name=resource_name) if plugin else None

    def get(self, user_identifier, resource_name, identifier=None, filter=None):
        """
        """
        plugin = self._managing_plugin(resource_name=resource_name, identifier=identifier)
        return plugin.get(user_identifier=user_identifier, resource_name=resource_name, identifier=identifier, filter=filter) if plugin else None

    def get_all(self, user_identifier, parent, resource_name, page=None, page_size=None, filter=None, order_by=None):
        """
        """
        plugin = self._managing_plugin(resource_name=resource_name, identifier=None)
        return plugin.get_all(user_identifier=user_identifier, parent=parent, resource_name=resource_name, page=page, page_size=page_size, filter=filter, order_by=order_by) if plugin else None

    def create(self, user_identifier, resource, parent=None):
        """
        """
        plugin = self._managing_plugin(resource_name=resource.rest_name, identifier=resource.id)
        return plugin.create(user_identifier=user_identifier, resource=resource, parent=parent) if plugin else None

    def update(self, user_identifier, resource):
        """
        """
        plugin = self._managing_plugin(resource_name=resource.rest_name, identifier=resource.id)
        return plugin.update(user_identifier=user_identifier, resource=resource) if plugin else None

    def delete(self, user_identifier, resource, cascade=True):
        """
        """
        plugin = self._managing_plugin(resource_name=resource.rest_name, identifier=resource.id)
        return plugin.delete(user_identifier=user_identifier, resource=resource, cascade=cascade) if plugin else None

    def delete_multiple(self, user_identifier, resources, cascade=True):
        """
        """
        plugin = self._managing_plugin(resource_name=resources[0].rest_name)
        return plugin.delete_multiple(user_identifier=user_identifier, resources=resources, cascade=cascade) if plugin else None

    def assign(self, user_identifier, resource_name, resources, parent):
        """
        """
        plugin = self._managing_plugin(resource_name=resource_name, identifier=None)
        return plugin.assign(user_identifier=user_identifier, resource_name=resource_name, resources=resources, parent=parent) if plugin else None

    def count(self, user_identifier, parent, resource_name, filter=None):
        """
        """
        plugin = self._managing_plugin(resource_name=resource_name, identifier=None)
        return plugin.count(user_identifier=user_identifier, parent=parent, resource_name=resource_name, filter=filter) if plugin else None

    # Utils

    def _managing_plugin(self, resource_name, identifier=None):
        """
        """
        if resource_name in self._managing_plugin_registry:
            return self._managing_plugin_registry[resource_name]

        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=identifier):
                self._managing_plugin_registry[resource_name] = plugin
                return plugin

        return None  # pragma: no cover
