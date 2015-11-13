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
        self.user_identifier = None

    def run(self):
        """
        """
        action = self.context.request.action
        resources = self.context.request.resources

        self.user_identifier = self.context.session.root_object.id if self.context.session.root_object else 'system'

        if len(resources) == 2:
            parent_resource = resources[0]
            response = self.storage_controller.get(user_identifier=self.user_identifier,
                                                   resource_name=parent_resource.name,
                                                   identifier=parent_resource.value)

            if response.has_errors:
                self.context.add_errors(response.errors)
                return

            self.context.parent_object = response.data

        if action is GARequest.ACTION_READALL:
            self._perform_readall_operation(count_only=False)

        elif action is GARequest.ACTION_COUNT:
            self._perform_readall_operation(count_only=True)

        elif action is GARequest.ACTION_READ:
            self._perform_read_operation()

        elif action in (GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE, GARequest.ACTION_DELETE, GARequest.ACTION_ASSIGN):
            self._perform_write_operation()

        else:
            raise Exception('Unknown action %s.' % action)

    # UTILITIES

    def _populate_parent_object_if_needed(self):
        """
        """
        if not self.context.parent_object and (self.context.object and self.context.object.parent_type and self.context.object.parent_id):

            response = self.storage_controller.get(user_identifier=self.user_identifier,
                                                   resource_name=self.context.object.parent_type,
                                                   identifier=self.context.object.parent_id)

            if response.has_errors:
                self.context.add_errors(response.errors)
                return

            self.context.parent_object = response.data

    # READ OPERATIONS

    def _prepare_context_for_read_operation(self):
        """
        """
        resource = self.context.request.resources[-1]

        response = self.storage_controller.get(user_identifier=self.user_identifier,
                                               resource_name=resource.name,
                                               identifier=resource.value)

        if response.has_errors:
            self.context.add_errors(response.errors)
            return

        self.context.object = response.data

    def _perform_read_operation(self):
        """
        """
        if self.context.object is None:
            self._prepare_context_for_read_operation()

        if self.context.has_errors:
            return

        self._populate_parent_object_if_needed()

        self.logic_controller.perform_delegate(delegate='will_perform_read', context=self.context)

        if self.context.has_errors:
            return

        self.logic_controller.perform_delegate(delegate='did_perform_read', context=self.context)

    # READALL OPERATIONS

    def _prepare_context_for_readall_operation(self, count_only):
        """
        """
        resource = self.context.request.resources[-1]

        if count_only:
            response = self.storage_controller.count(user_identifier=self.user_identifier,
                                                     parent=self.context.parent_object,
                                                     resource_name=resource.name,
                                                     filter=self.context.request.filter)

            if response.has_errors:
                self.context.add_errors(response.errors)
                return

            self.context.total_count = response.count
        else:
             response = self.storage_controller.get_all(user_identifier=self.user_identifier,
                                                        parent=self.context.parent_object,
                                                        resource_name=resource.name,
                                                        page=self.context.request.page,
                                                        page_size=self.context.request.page_size,
                                                        filter=self.context.request.filter,
                                                        order_by=self.context.request.order_by)

             if response.has_errors:
                 self.context.add_errors(response.errors)
                 return

             self.context.objects = response.data
             self.context.total_count = response.count

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
        self.context.object = self.storage_controller.instantiate(resource_name=resource.name)

        if not self.context.object:
            self.context.add_error(GAError(type=GAError.TYPE_INVALID,
                                           title='Bad request',
                                           description='Could not find object of type %s in the models' % resource.name))
            return

        self.context.object.from_dict(self.context.request.content)

    def _populate_context_for_update_with_resource(self, resource):
        """
        """
        response = self.storage_controller.get(user_identifier=self.user_identifier,
                                               resource_name=resource.name,
                                               identifier=resource.value)

        if response.has_errors:
            self.context.add_errors(response.errors)
            return

        self.context.object = response.data
        self.context.object.from_dict(self.context.request.content)

    def _populate_context_for_delete_with_resource(self, resource):
        """
        """
        response = self.storage_controller.get(user_identifier=self.user_identifier,
                                               resource_name=resource.name,
                                               identifier=resource.value)

        if response.has_errors:
            self.context.add_errors(response.errors)
            return

        self.context.object = response.data

    def _populate_context_for_assign_with_resource(self, resource):
        """
        """
        for object_id in self.context.request.content:

            response = self.storage_controller.get(user_identifier=self.user_identifier,
                                                   resource_name=resource.name,
                                                   identifier=object_id)
            if response.has_errors:
                self.context.add_errors(response.errors)
                continue

            self.context.objects.append(response.data)

    def _prepare_context_for_write_operation(self):
        """
        """
        action = self.context.request.action
        resource = self.context.request.resources[-1]

        if action != GARequest.ACTION_CREATE and action != GARequest.ACTION_ASSIGN and resource.value is None:
            self.context.add_error(GAError(type=GAError.TYPE_NOTALLOWED,
                                           title='Action not allowed',
                                           description='Unable to %s a resource without its identifier' % action))
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
        action = self.context.request.action

        if action == GARequest.ACTION_CREATE:
            response = self.storage_controller.create(user_identifier=self.user_identifier,
                                                      resource=self.context.object,
                                                      parent=self.context.parent_object)

        elif action == GARequest.ACTION_UPDATE:
            response = self.storage_controller.update(user_identifier=self.user_identifier,
                                                      resource=self.context.object)

        elif action == GARequest.ACTION_DELETE:
            response = self.storage_controller.delete(user_identifier=self.user_identifier,
                                                      resource=self.context.object,
                                                      cascade=True)

        elif action == GARequest.ACTION_ASSIGN:
            response = self.storage_controller.assign(user_identifier=self.user_identifier,
                                                      resource_name=self.context.request.resources[-1].name,
                                                      resources=self.context.objects,
                                                      parent=self.context.parent_object)

        if response.has_errors:
            self.context.add_errors(response.errors)

    def _perform_push(self):
        """
        """
        if self.context.request.action == GARequest.ACTION_ASSIGN:
            self.context.add_event(GAPushEvent(action=self.context.request.action,
                                               entity=self.context.parent_object))
        else:
            self.context.add_event(GAPushEvent(action=self.context.request.action,
                                               entity=self.context.object))
