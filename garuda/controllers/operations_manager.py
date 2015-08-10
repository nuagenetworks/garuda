# -*- coding: utf-8 -*-

from garuda.models import GARequest
from .models_controller import ModelsController
from .plugins_manager import PluginsManager
from garuda.exceptions import NotFoundException, BadRequestException, ActionNotAllowedException


class OperationsManager(object):
    """

    """
    def __init__(self, context):
        """
        """
        self.context = context

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

        self.context.object = ModelsController.get_object(resource.name, resource.value)

    def _perform_read_operation(self):
        """
        """
        self._prepare_context_for_read_operation()

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_read_operation')

        # Manage one object at a time
        plugin_manager.perform_delegate(delegate='should_perform_read', object=self.context.object)

        if len(self.context.errors) > 0:
            raise BadRequestException()

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
            parent = ModelsController.get_current_user()

        else:  # Having a parent and a child
            parent_resource = resources[0]
            parent = ModelsController.get_object(parent_resource.name, parent_resource.value)

            if parent is None:
                description = 'Unable to retrieve object parent %s with identifier %s' % (parent_resource.name, parent_resource.value)
                self.context.report_error(property='', title='Object not found', description=description)
                raise NotFoundException()

        self.context.parent = parent
        self.context.objects = ModelsController.get_objects(parent, resource.name)

    def _perform_readall_operation(self):
        """
        """
        self._prepare_context_for_read_operation()

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_readall_operation')

        for object in self.context.objects:
            # Manage one object at a time
            plugin_manager.perform_delegate(delegate='should_perform_readall', object=object)

            if len(self.context.errors) > 0:
                raise BadRequestException()

                plugin_manager.perform_delegate(delegate='preprocess_readall', object=object)
            # End manage

        # ModelsController.read()

        plugin_manager.perform_delegate(delegate='end_readall_operation')



    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources
        resource = resources[-1]

        if action != GARequest.ACTION_CREATE and resource.value is None:
            description = 'Unable to %s a resource without its identifier' % self.context.action
            self.context.report_error(property='', title='Action not allowed', description=description)
            raise ActionNotAllowedException()

        if len(resources) == 1:
            parent = None

        else:  # Having a parent and a child
            parent_resource = resources[0]
            self.context.parent = ModelsController.get_object(parent_resource.name, parent_resource.value)

            if parent is None:
                description = 'Unable to retrieve object parent %s with identifier %s' % (parent_resource.name, parent_resource.value)
                self.context.report_error(property='', title='Object not found', description=description)
                raise NotFoundException()

        if action == GARequest.ACTION_CREATE:
            self.context.object = ModelsController.create_object(resource.name)
        else:
            self.context.object = ModelsController.get_object(resource.name, resource.value)

    def _perform_write_operation(self):
        """
        """
        self._prepare_context_for_write_operation()

        # Do a read after all
        pass
