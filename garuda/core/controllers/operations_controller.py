# -*- coding: utf-8 -*-

from garuda.core.models import GARequest, GAError, GAPushEvent
from .logic_plugins_controller import GALogicPluginsController

class GAOperationsController(object):
    """

    """
    def __init__(self, context, model_controller):
        """
        """
        self.context = context
        self.model_controller = model_controller

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

        self.context.object = self.model_controller.get(resource.name, resource.value)

        if self.context.object is None:
            error = GAError(type=GAError.TYPE_NOTFOUND,
                            title='%s not found' % resource.name,
                            description='Cannot find %s with ID %s' % (resource.name, resource.value))

            self.context.report_error(error)

    def _perform_read_operation(self):
        """
        """
        if self.context.object is None:
            self._prepare_context_for_read_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_read_operation')

        # Manage one object at a time
        logic_plugins_controller.perform_delegate(delegate='should_perform_read', object=self.context.object)

        if self.context.has_errors():
            return

        logic_plugins_controller.perform_delegate(delegate='preprocess_read')
        # End manage

        logic_plugins_controller.perform_delegate(delegate='end_read_operation')

    def _prepare_context_for_readall_operation(self):
        """
        """
        resources = self.context.request.resources
        resource = resources[-1]

        if len(resources) == 1:
            # Root parent
            parent = None

        else:  # Having a parent and a child
            parent_resource = resources[0]

            parent = self.model_controller.get(parent_resource.name, parent_resource.value)

            if parent is None:

                error = GAError( type=GAError.TYPE_NOTFOUND,
                                 title='Object not found',
                                 description='Unable to retrieve object parent %s with identifier %s' % (parent_resource.name, parent_resource.value))

                self.context.report_error(error)
                return

        self.context.parent = parent
        self.context.objects = self.model_controller.get_all(parent, resource.name)

        if self.context.objects is None:

            error = GAError(type=GAError.TYPE_NOTFOUND,
                            title='Objects not found',
                            description='Could not find any %s' % resource.name)

            self.context.report_error(error)

    def _perform_readall_operation(self):
        """
        """
        self._prepare_context_for_readall_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_readall_operation')

        for object in self.context.objects:
            # Manage one object at a time
            logic_plugins_controller.perform_delegate(delegate='should_perform_readall', object=object)

            if self.context.has_errors():
                return

            logic_plugins_controller.perform_delegate(delegate='preprocess_readall', object=object)
            # End manage

        logic_plugins_controller.perform_delegate(delegate='end_readall_operation')

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources
        resource = resources[-1]

        if action != GARequest.ACTION_CREATE and resource.value is None:

            error = GAError(type=GAError.TYPE_NOTFOUND,
                             title='Action not allowed',
                             description='Unable to %s a resource without its identifier' % self.context.request.action)

            self.context.report_error(error)
            return

        if len(resources) == 1:
            self.context.parent = None

        else:
            parent_resource = resources[0]

            self.context.parent = self.model_controller.get(parent_resource.name, parent_resource.value)

            if self.context.parent is None:

                error = GAError(type=GAError.TYPE_NOTFOUND,
                                 title='Object not found',
                                 description='Unable to retrieve object parent %s with ID %s' % (parent_resource.name, parent_resource.value))

                self.context.report_error(error)
                return

        if action == GARequest.ACTION_CREATE:
            self.context.object = self.model_controller.instantiate(resource.name)
        else:
            self.context.object = self.model_controller.get(resource.name, resource.value)

        if self.context.object is None:

            error = GAError(type=GAError.TYPE_NOTFOUND,
                             title='%s not found' % resource.name,
                             description='Cannot find %s with ID %s' % (resource.name, resource.value))

            self.context.report_error(error)

        elif not self.context.object.is_valid():

            for property_name, description in self.context.object.errors.iteritems():

                error = GAError(type=GAError.TYPE_INVALID,
                                title='Invalid %s' % property_name,
                                description=description,
                                property_name=property_name)

                self.context.report_error(error)

    def _perform_write_operation(self):
        """
        """
        self._prepare_context_for_write_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_write_operation')

        logic_plugins_controller.perform_delegate(delegate='should_perform_write')

        if self.context.has_errors():
            return

        logic_plugins_controller.perform_delegate(delegate='preprocess_write')

        err = None
        if self.context.request.action == GARequest.ACTION_DELETE:
            err = self.model_controller.delete(resource=self.context.object)

        elif self.context.request.action == GARequest.ACTION_CREATE:
            self.context.object.from_dict(self.context.request.content)
            err = self.model_controller.create(resource=self.context.object, parent=self.context.parent)

        elif self.context.request.action == GARequest.ACTION_UPDATE:
            self.context.object.from_dict(self.context.request.content)
            err = self.model_controller.update(resource=self.context.object)

        if err:
            if isinstance(err, list):
                self.context.report_errors(err)
            else:
                self.context.report_error(err)
            return

        if not self.context.object.is_valid():

            for property_name, description in self.context.object.errors.iteritems():

                error = GAError(type=GAError.TYPE_INVALID,
                                title='Invalid %s' % property_name,
                                description=description,
                                property_name=property_name)

                self.context.report_error(error)

            return

        logic_plugins_controller.perform_delegate(delegate='did_perform_write')

        logic_plugins_controller.perform_delegate(delegate='end_write_operation')

        self.context.add_event(GAPushEvent(action=self.context.request.action, entity=self.context.object))
