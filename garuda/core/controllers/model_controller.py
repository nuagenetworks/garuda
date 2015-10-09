# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('garuda.modelcontroller')

from garuda.core.controllers.abstracts import GAPluginController
from garuda.core.plugins import GAModelControllerPlugin


class GAModelController(GAPluginController):
    """

    """
    def __init__(self, plugins, core_controller):
        """
        """
        super(GAModelController, self).__init__(plugins=plugins, core_controller=core_controller)

    # Override

    def register_plugin(self, plugin):
        """
        """
        super(GAModelController, self).register_plugin(plugin=plugin, plugin_type=GAModelControllerPlugin)

    # Implementation

    def instantiate(self, resource_name):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=None):
                return plugin.instantiate(resource_name=resource_name)

        return None

    def get(self, resource_name, identifier):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=identifier):
                return plugin.get(resource_name=resource_name, identifier=identifier)

        return None

    def get_all(self, parent, resource_name):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource_name, identifier=None):
                return plugin.get_all(parent=parent, resource_name=resource_name)

        return None

    def create(self, resource, parent=None):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource.rest_resource_name, identifier=resource.id):
                return plugin.create(resource=resource, parent=parent)

        return None

    def update(self, resource):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource.rest_resource_name, identifier=resource.id):
                return plugin.update(resource=resource)

        return None

    def delete(self, resource):
        """
        """
        for plugin in self._plugins:
            if plugin.should_manage(resource_name=resource.rest_resource_name, identifier=resource.id):
                return plugin.delete(resource=resource)

        return None
