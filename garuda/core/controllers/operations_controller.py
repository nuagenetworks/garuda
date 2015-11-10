# -*- coding: utf-8 -*-

from garuda.core.models import GARequest, GAError, GAPushEvent


class GAOperationsController(object):
    """
    """
    def __init__(self, context, logic_controller, storage_controller):
        """
        """
        self.context = context
        self.storage_controller = storage_controller
        self.logic_controller = logic_controller

    def run(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources

        if len(resources) == 2:
            parent_resource = resources[0]
            self.context.parent_object = self.storage_controller.get(parent_resource.name, parent_resource.value)

            if self.context.parent_object is None:
                self._report_resource_not_found(resource=parent_resource)
                return

        if action is GARequest.ACTION_READALL:
            self._perform_readall_operation(count_only=False)

        elif action is GARequest.ACTION_COUNT:
            self._perform_readall_operation(count_only=True)

        elif action is GARequest.ACTION_READ:
            self._perform_read_operation()

        elif action in (GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_DELETE, GARequest.ACTION_ASSIGN):
            self._perform_write_operation()

        else:
            raise Exception('action %s does not exist.' % action)

    # UTILITIES

    def _report_resource_not_found(self, resource):
        """
        """
        self.context.add_error(GAError(type=GAError.TYPE_NOTFOUND,
                                       title='%s not found' % resource.name,
                                       description='Cannot find %s with ID %s' % (resource.name, resource.value)))

    def _report_validation_error(self, resource):
        """
        """
        for property_name, description in resource.errors.iteritems():
            self.context.add_error(GAError(type=GAError.TYPE_CONFLICT,
                                           title='Invalid %s' % property_name,
                                           description=description,
                                           property_name=property_name))

    def _report_method_not_allowed(self, action):
        """
        """
        self.context.add_error(GAError(type=GAError.TYPE_NOTALLOWED,
                                       title='Action not allowed',
                                       description='Unable to %s a resource without its identifier' % action))

    def _populate_parent_object_if_needed(self):
        """
        """
        if not self.context.parent_object and (self.context.object and self.context.object.parent_type and self.context.object.parent_id):
            self.context.parent_object = self.storage_controller.get(self.context.object.parent_type, self.context.object.parent_id)

    # READ OPERATIONS

    def _prepare_context_for_read_operation(self):
        """
        """
        resource = self.context.request.resources[-1]

        self.context.object = self.storage_controller.get(resource.name, resource.value)

        if self.context.object is None:
            self._report_resource_not_found(resource=resource)

    def _perform_read_operation(self):
        """
        """

        # the object may already be set in case of a read operation
        # triggered by a push notification. In that case, there is no
        # need to query the DB again.
        if self.context.object is None:
            self._prepare_context_for_read_operation()

        if self.context.has_errors:
            return

        self._populate_parent_object_if_needed()

        self.logic_controller.perform_delegate(delegate='will_perform_read', context=self.context)

        if self.context.has_errors:
            return

        self.logic_controller.perform_delegate(delegate='did_perform_read', context=self.context)

    def _prepare_context_for_readall_operation(self, count_only):
        """
        """
        resource = self.context.request.resources[-1]

        if count_only:
            self.context.total_count = self.storage_controller.count(parent=self.context.parent_object,
                                                                     resource_name=resource.name,
                                                                     filter=self.context.request.filter)
        else:
            self.context.objects, self.context.total_count = self.storage_controller.get_all(parent=self.context.parent_object,
                                                                                             resource_name=resource.name,
                                                                                             page=self.context.request.page,
                                                                                             page_size=self.context.request.page_size,
                                                                                             filter=self.context.request.filter,
                                                                                             order_by=self.context.request.order_by)

        if self.context.objects is None:
            self._report_resource_not_found(resource=resource)

    def _perform_readall_operation(self, count_only):
        """
        """
        self._prepare_context_for_readall_operation(count_only)

        if self.context.has_errors:
            return

        self._populate_parent_object_if_needed()

        self.logic_controller.perform_delegate(delegate='will_perform_readall', context=self.context)

        if self.context.has_errors:
            return

        self.logic_controller.perform_delegate(delegate='did_perform_readall', context=self.context)

    # WRITE OPERATIONS

    def _populate_context_for_create_with_resource(self, resource):
        """
        """
        self.context.object = self.storage_controller.instantiate(resource.name)

        if self.context.object is None:
            self._report_resource_not_found(resource=resource)
            return

        self.context.object.from_dict(self.context.request.content)

    def _populate_context_for_update_with_resource(self, resource):
        """
        """
        self.context.object = self.storage_controller.get(resource.name, resource.value)

        if self.context.object is None:
            self._report_resource_not_found(resource=resource)
            return

        self.context.object.from_dict(self.context.request.content)

    def _populate_context_for_delete_with_resource(self, resource):
        """
        """
        self.context.object = self.storage_controller.get(resource.name, resource.value)

        if self.context.object is None:
            self._report_resource_not_found(resource=resource)

    def _populate_context_for_assign_with_resource(self, resource):
        """
        """
        for object_id in self.context.request.content:
            assigned_object = self.storage_controller.get(resource.name, object_id)

            if not assigned_object:
                self._report_resource_not_found(resource=resource)
                continue

            self.context.objects.append(assigned_object)

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resource = self.context.request.resources[-1]

        if action != GARequest.ACTION_CREATE and action != GARequest.ACTION_ASSIGN and resource.value is None:
            self._report_method_not_allowed(action=self.context.request.action)
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

        if self.context.has_errors:
            return

        self._populate_parent_object_if_needed()

        action_name = self.context.request.action.lower()

        self.logic_controller.perform_delegate(delegate='will_perform_write', context=self.context)
        self.logic_controller.perform_delegate(delegate='will_perform_%s' % action_name, context=self.context)

        if self.context.has_errors:
            return

        self._perform_store()

        if self.context.has_errors:
            return

        self.logic_controller.perform_delegate(delegate='did_perform_%s' % action_name, context=self.context)
        self.logic_controller.perform_delegate(delegate='did_perform_write', context=self.context)

        self._perform_push()

    def _perform_store(self):
        """
        """
        err = None
        action = self.context.request.action

        if action == GARequest.ACTION_CREATE:
            err = self.storage_controller.create(resource=self.context.object,
                                                 parent=self.context.parent_object)

        elif action == GARequest.ACTION_UPDATE:
            err = self.storage_controller.update(resource=self.context.object)

        elif action == GARequest.ACTION_DELETE:
            err = self.storage_controller.delete(resource=self.context.object,
                                                 cascade=True)

        elif action == GARequest.ACTION_ASSIGN:
            err = self.storage_controller.assign(resource_name=self.context.request.resources[-1].name,
                                                 resources=self.context.objects,
                                                 parent=self.context.parent_object)

        if err:
            if isinstance(err, list):
                self.context.add_errors(err)
            else:
                self.context.add_error(err)

    def _perform_push(self):
        """
        """
        if self.context.request.action == GARequest.ACTION_ASSIGN:
            self.context.add_event(GAPushEvent(action=self.context.request.action,
                                               entity=self.context.parent_object))
        else:
            self.context.add_event(GAPushEvent(action=self.context.request.action,
                                               entity=self.context.object))
