# -*- coding: utf-8 -*-

from garuda.models import GASession
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
        action = self.context.session.action

        if action is GASession.ACTION_READALL or action is GASession.ACTION_READ:
            self._perform_read_operation()
        else:
            self._perform_write_operation()

    def _prepare_context_for_read_operation(self):
        """
        """
        action = self.context.session.action
        resources = self.context.session.resources
        resource = resources[-1]

        if action == GASession.ACTION_READALL:
            # Get all resources
            if len(resources) == 1:
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

        else:
            # Get a specific resource.name
            self.context.object = ModelsController.get_object(resource.name, resource.value)

    def _perform_read_operation(self):
        """

        """
        self._prepare_context_for_read_operation()

        plugin_manager = PluginsManager(context=self.context)

        plugin_manager.perform_delegate(delegate='begin_read_operation')

        plugin_manager.perform_delegate(delegate='should_perform_read')

        if len(self.context.errors) > 0:
            raise BadRequestException()

        plugin_manager.perform_delegate(delegate='preprocess_read')

        ModelsController.read()

        plugin_manager.perform_delegate(delegate='end_read_operation')

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.session.action
        resources = self.context.session.resources
        resource = resources[-1]

        if action != GASession.ACTION_CREATE and resource.value is None:
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

        if action == GASession.ACTION_CREATE:
            self.context.object = ModelsController.create_object(resource.name)
        else:
            self.context.object = ModelsController.get_object(resource.name, resource.value)

    def _perform_write_operation(self):
        """
        """
        self._prepare_context_for_write_operation()
        pass