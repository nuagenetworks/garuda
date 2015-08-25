# -*- coding: utf-8 -*-

from garuda.models import GARequest, GAError
from .models_controller import ModelsController
from .plugins_manager import PluginsManager


class OperationsManager(object):
    """

    """
    def __init__(self, context, models_controller):
        """
        """
        self.context = context
        self.models_controller = models_controller

    def run(self):
        """
        """
        action = self.context.request.action

        if action is GARequest.ACTION_READALL:
            self._perform_readall_operation()

        elif action is GARequest.ACTION_READ:
            self._perform_read_operation()

        else:
            self._perform_write_operation()


    def _prepare_context_for_read_operation(self):
        """
        """
        resources = self.context.request.resources
        resource = resources[-1]

        self.context.object = self.models_controller.get_object(resource.name, resource.value)

        if self.context.object is None:
            self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Object not found', description='Could not find %s with identifier %s' % (resource.name, resource.value))

    def _perform_read_operation(self):
        """
        """

        self._prepare_context_for_read_operation()

        if self.context.has_errors():
            return

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_read_operation')

        # Manage one object at a time
        plugin_manager.perform_delegate(delegate='should_perform_read', object=self.context.object)

        if self.context.has_errors():
            return

        plugin_manager.perform_delegate(delegate='preprocess_read')
        # End manage

        plugin_manager.perform_delegate(delegate='end_read_operation')

    def _prepare_context_for_readall_operation(self):
        """
        """
        resources = self.context.request.resources
        resource = resources[-1]

        if len(resources) == 1:
            # Root parent
            parent = self.models_controller.get_current_user()

        else:  # Having a parent and a child
            parent_resource = resources[0]

            parent = self.models_controller.get_object(parent_resource.name, parent_resource.value)

            if parent is None:
                description = 'Unable to retrieve object parent %s with identifier %s' % (parent_resource.name, parent_resource.value)
                self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Object not found', description=description)
                return

        self.context.parent = parent
        self.context.objects = self.models_controller.get_objects(parent, resource.name)

        if self.context.objects is None:
            self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Objects not found', description='Could not find any %s' % resource.name)

    def _perform_readall_operation(self):
        """
        """
        self._prepare_context_for_readall_operation()

        if self.context.has_errors():
            return

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_readall_operation')

        for object in self.context.objects:
            # Manage one object at a time
            plugin_manager.perform_delegate(delegate='should_perform_readall', object=object)

            if self.context.has_errors():
                return

            plugin_manager.perform_delegate(delegate='preprocess_readall', object=object)
            # End manage

        plugin_manager.perform_delegate(delegate='end_readall_operation')

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources
        resource = resources[-1]

        if action != GARequest.ACTION_CREATE and resource.value is None:
            description = 'Unable to %s a resource without its identifier' % self.context.request.action
            self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Action not allowed', description=description)
            return

        if len(resources) == 1:
            self.context.parent = self.models_controller.get_current_user()

        else:  # Having a parent and a child
            parent_resource = resources[0]

            self.context.parent = self.models_controller.get_object(parent_resource.name, parent_resource.value)

            if parent is None:
                description = 'Unable to retrieve object parent %s with identifier %s' % (parent_resource.name, parent_resource.value)
                self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Object not found', description=description)
                return

        if action == GARequest.ACTION_CREATE:
            self.context.object = self.models_controller.create_object(resource.name)
        else:
            self.context.object = self.models_controller.get_object(resource.name, resource.value)

        if self.context.object is None:
            description = 'Unable to retrieve object %s with identifier %s' % (resource.name, resource.value)
            self.context.report_error(type=GAError.TYPE_NOTFOUND, property='', title='Object not found', description=description)

        elif not self.context.object.is_valid():
            for property, description in self.context.object.errors.iteritems():
                self.context.report_error(type=GAError.TYPE_INVALID, property=property, title='Invalid %s' % property, description=description)

    def _perform_write_operation(self):
        """
        """
        self._prepare_context_for_write_operation()

        if self.context.has_errors():
            return

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_write_operation')

        plugin_manager.perform_delegate(delegate='should_perform_write')

        if self.context.has_errors():
            return

        plugin_manager.perform_delegate(delegate='preprocess_write')

        if self.context.request.action == GARequest.ACTION_DELETE:
            self.models_controller.delete_object(object=self.context.object)
        else:
            self.models_controller.save_object(object=self.context.object, parent=self.context.parent, attributes=self.context.request.content)

        if not self.context.object.is_valid():
            for property, description in self.context.object.errors.iteritems():
                self.context.report_error(type=GAError.TYPE_INVALID, property=property, title='Invalid %s' % property, description=description)
            return

        plugin_manager.perform_delegate(delegate='did_perform_write')

        plugin_manager.perform_delegate(delegate='end_write_operation')
