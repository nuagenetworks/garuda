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

    ## UTILITIES

    def _report_resource_not_found(self, resource):
        """
        """
        self.context.report_error(GAError(  type=GAError.TYPE_NOTFOUND,
                                            title='%s not found' % resource.name,
                                            description='Cannot find %s with ID %s' % (resource.name, resource.value)))


    def _report_validation_error(self, resource):
        """
        """
        for property_name, description in resource.errors.iteritems():
            self.context.report_error(GAError(  type=GAError.TYPE_INVALID,
                                                title='Invalid %s' % property_name,
                                                description=description,
                                                property_name=property_name))

    def _report_method_not_allowed(self, action):
        """
        """
        self.context.report_error(GAError(  type=GAError.TYPE_NOTFOUND,
                                            title='Action not allowed',
                                            description='Unable to %s a resource without its identifier' % action)
)

    ## READ OPERATIONS

    def _prepare_context_for_read_operation(self):
        """
        """
        resources = self.context.request.resources
        resource = resources[-1]

        self.context.object = self.model_controller.get(resource.name, resource.value)

        if self.context.object is None: self._report_resource_not_found(resource=resource)


    def _perform_read_operation(self):
        """
        """
        # TODO ANTOINE: can the context be already set to something from here?
        if self.context.object is None:
            self._prepare_context_for_read_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_read_operation')
        logic_plugins_controller.perform_delegate(delegate='should_perform_read', object=self.context.object)

        if self.context.has_errors():
            return

        logic_plugins_controller.perform_delegate(delegate='preprocess_read')
        logic_plugins_controller.perform_delegate(delegate='end_read_operation')

    def _prepare_context_for_readall_operation(self):
        """
        """
        resources = self.context.request.resources
        resource = resources[-1]
        parent = None

        if len(resources) != 1:
            parent_resource = resources[0]

            parent = self.model_controller.get(parent_resource.name, parent_resource.value)

            if parent is None:
                self._report_resource_not_found(resources=parent_resource)
                return

        self.context.parent_object = parent
        self.context.objects = self.model_controller.get_all(self.context.parent_object, resource.name)

        if self.context.objects is None: self._report_resource_not_found(resource=resource)

    def _perform_readall_operation(self):
        """
        """
        self._prepare_context_for_readall_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_readall_operation')

        for obj in self.context.objects:

            logic_plugins_controller.perform_delegate(delegate='should_perform_readall', object=obj)

            if self.context.has_errors():
                return

            logic_plugins_controller.perform_delegate(delegate='preprocess_readall', object=obj)

        logic_plugins_controller.perform_delegate(delegate='end_readall_operation')


    ## WRITE OPERATIONS

    def _populate_context_for_create_with_resource(self, resource):
        """
        """
        self.context.object = self.model_controller.instantiate(resource.name)

        if self.context.object is None: self._report_resource_not_found(resource=resource)

        self.context.object.from_dict(self.context.request.content)

        if not self.context.object.is_valid(): self._report_validation_error(self.context.object)


    def _populate_context_for_update_with_resource(self, resource):
        """
        """
        self.context.object = self.model_controller.get(resource.name, resource.value)

        if self.context.object is None: self._report_resource_not_found(resource=resource)

        self.context.object.from_dict(self.context.request.content)

        if not self.context.object.is_valid(): self._report_validation_error(self.context.object)

    def _populate_context_for_delete_with_resource(self, resource):
        """
        """
        self.context.object = self.model_controller.get(resource.name, resource.value)

        if self.context.object is None: self._report_resource_not_found(resource=resource)


    def _populate_context_for_assign_with_resource(self, resource):
        """
        """
        for object_id in self.context.request.content:
            assigned_object = self.model_controller.get(resource.name, object_id)

            if not assigned_object:
                self._report_resource_not_found(resource=resource)
                continue

            self.context.objects.append(assigned_object)

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources
        resource = resources[-1]

        if action != GARequest.ACTION_CREATE and action != GARequest.ACTION_ASSIGN and resource.value is None:
            self._report_method_not_allowed(action=self.context.request.action)
            return

        if len(resources) != 1:
            parent_resource = resources[0]

            self.context.parent_object = self.model_controller.get(parent_resource.name, parent_resource.value)

            if self.context.parent_object is None:
                self._report_resource_not_found(resource=parent_resource)
                return

        if action == GARequest.ACTION_CREATE:
            self._populate_context_for_create_with_resource(resource=resource)

        elif action == GARequest.ACTION_UPDATE:
            self._populate_context_for_update_with_resource(resource=resource)

        elif action == GARequest.ACTION_DELETE:
            self._populate_context_for_delete_with_resource(resource=resource)

        elif action == GARequest.ACTION_ASSIGN:
            self._populate_context_for_assign_with_resource(resource=resource)

    def _perform_write_operation(self):
        """
        """
        self._prepare_context_for_write_operation()

        if self.context.has_errors():
            return

        logic_plugins_controller = GALogicPluginsController(context=self.context)

        logic_plugins_controller.perform_delegate(delegate='begin_write_operation')
        logic_plugins_controller.perform_delegate(delegate='should_perform_write')

        if self.context.has_errors(): return

        logic_plugins_controller.perform_delegate(delegate='preprocess_write')

        err = None

        if self.context.request.action == GARequest.ACTION_CREATE:
            err = self.model_controller.create(resource=self.context.object, parent=self.context.parent_object)

        elif self.context.request.action == GARequest.ACTION_UPDATE:
            err = self.model_controller.update(resource=self.context.object)

        elif self.context.request.action == GARequest.ACTION_DELETE:
            err = self.model_controller.delete(resource=self.context.object)

        elif self.context.request.action == GARequest.ACTION_ASSIGN:
            err = self.model_controller.assign(resource_name=self.context.request.resources[-1], resources=self.context.objects, parent=self.context.parent_object)

        if err:
            if isinstance(err, list):
                self.context.report_errors(err)
            else:
                self.context.report_error(err)
            return

        logic_plugins_controller.perform_delegate(delegate='did_perform_write')

        logic_plugins_controller.perform_delegate(delegate='end_write_operation')

        self.context.add_event(GAPushEvent(action=self.context.request.action, entity=self.context.object))
