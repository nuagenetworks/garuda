# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch

from garuda.core.controllers import GAOperationsController
from garuda.core.models import GAContext, GASession, GARequest, GAResource, GAError

import tests.tstdk.v1_0 as tstdk


class FakeLogicController(object):
    """
    """

    def perform_delegate(self, delegate, context):
        context.performed_delegates.append(delegate)


class FakeStorageController(object):
    """
    """
    def instantiate(self, resource_name):
        pass

    def get(self, resource_name, identifier):
        pass

    def get_all(self, parent, resource_name, page, page_size, filter, order_by):
        pass

    def count(self):
        pass

    def create(self, resource, parent):
        pass

    def update(self, resource):
        pass

    def delete(self, resource, cascade):
        pass

    def assign(self, resource_name, resources, parent):
        pass


class TestOperationsController(TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """
        """
        cls.fake_logic_controller = FakeLogicController()
        cls.fake_storage_controller = FakeStorageController()

    def test_initialization(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        self.assertEquals(operations_controller.context, context)
        self.assertEquals(operations_controller.logic_controller, self.fake_logic_controller)
        self.assertEquals(operations_controller.storage_controller, self.fake_storage_controller)

    def test_report_resource_not_found(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller._report_resource_not_found(resource=GAResource(name='toto', value='value'))
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)

    def test_report_validation_error(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        enterprise1 = tstdk.GAEnterprise(name=None)
        context.object = enterprise1
        enterprise1.validate()

        operations_controller._report_validation_error(resource=enterprise1)
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_CONFLICT)

    def test_report_method_not_allowed(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller._report_method_not_allowed(action=GARequest.ACTION_UPDATE)
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTALLOWED)

    def test_populate_parent_object_if_needed(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        enterprise1.parent_type = 'fake'
        enterprise1.parent_id = 'yyyy'
        context.object = enterprise1

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAUser(username='test')):
            operations_controller._populate_parent_object_if_needed()

        self.assertEquals(context.parent_object.username, 'test')
        self.assertEquals(context.parent_object.rest_name, 'user')

    def test_run_with_parent_not_found(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=None):
            operations_controller.run()
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)

    def test_run_readall(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self, count_only):
                assert self.context.request.action == GARequest.ACTION_READALL
                self.context.object = 'did_read_all'

            with patch.object(GAOperationsController, '_perform_readall_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_read_all')

    def test_run_count(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_COUNT)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self, count_only):
                assert count_only
                assert self.context.request.action == GARequest.ACTION_COUNT
                self.context.object = 'did_read_all_with_count'

            with patch.object(GAOperationsController, '_perform_readall_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_read_all_with_count')

    def test_read(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                assert self.context.request.action == GARequest.ACTION_READ
                self.context.object = 'did_read'

            with patch.object(GAOperationsController, '_perform_read_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_read')

    def test_create(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                assert self.context.request.action == GARequest.ACTION_CREATE
                self.context.object = 'did_create'

            with patch.object(GAOperationsController, '_perform_write_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_create')

    def test_update(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                assert self.context.request.action == GARequest.ACTION_UPDATE
                self.context.object = 'did_update'

            with patch.object(GAOperationsController, '_perform_write_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_update')

    def test_delete(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_DELETE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                assert self.context.request.action == GARequest.ACTION_DELETE
                self.context.object = 'did_delete'

            with patch.object(GAOperationsController, '_perform_write_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_delete')

    def test_assign(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_ASSIGN)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                assert self.context.request.action == GARequest.ACTION_ASSIGN
                self.context.object = 'did_assign'

            with patch.object(GAOperationsController, '_perform_write_operation', autospec=True) as m:
                m.side_effect = mocked_method

                operations_controller.run()
                self.assertEquals(context.object, 'did_assign')

    def test_prepare_context_for_read_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_ASSIGN)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAUser(name='user1')):

            operations_controller._prepare_context_for_read_operation()
            self.assertEquals(len(context.errors), 0)

        with patch.object(self.fake_storage_controller, 'get', return_value=None):

            operations_controller._prepare_context_for_read_operation()
            self.assertEquals(len(context.errors), 1)

    def test_perform_read_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAUser(name='user1')):
            operations_controller._perform_read_operation()
            self.assertEquals(context.performed_delegates, ['begin_read_operation', 'check_perform_read', 'preprocess_read', 'end_read_operation'])

    def test_perform_read_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        context.performed_delegates = []
        context.add_error('fake')
        operations_controller._perform_read_operation()
        self.assertEquals(context.performed_delegates, [])

    def test_perform_read_operation_with_errors_in_the_middle(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAUser(name='user1')):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_read_operation()
                self.assertEquals(context.performed_delegates, ['begin_read_operation', 'check_perform_read'])

    def test_prepare_context_for_readall_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(FakeStorageController, 'count', return_value=42):
            operations_controller._prepare_context_for_readall_operation(count_only=True)
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.total_count, 42)

        with patch.object(FakeStorageController, 'get_all', return_value=([tstdk.GAUser(name='user1'), tstdk.GAUser(name='user2')], 2)):
            operations_controller._prepare_context_for_readall_operation(count_only=False)
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(len(context.objects), 2)
            self.assertEquals(context.total_count, 2)

        with patch.object(FakeStorageController, 'get_all', return_value=(None, 0)):
            operations_controller._prepare_context_for_readall_operation(count_only=False)
            self.assertEquals(len(context.errors), 1)

    def test_perform_readall_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get_all', return_value=([tstdk.GAUser(name='user1')], 1)):
            operations_controller._perform_readall_operation(count_only=False)
            self.assertEquals(context.performed_delegates, ['begin_readall_operation', 'check_perform_readall', 'preprocess_readall', 'end_readall_operation'])

    def test_perform_readall_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get_all', return_value=([tstdk.GAUser(name='user1')], 1)):
            context.performed_delegates = []
            context.add_error('fake')
            operations_controller._perform_readall_operation(count_only=False)
            self.assertEquals(context.performed_delegates, [])

    def test_perform_readall_operation_with_errors_in_the_middle(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(self.fake_storage_controller, 'get_all', return_value=([tstdk.GAUser(name='user1')], 1)):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_readall_operation(count_only=False)
                self.assertEquals(context.performed_delegates, ['begin_readall_operation', 'check_perform_readall'])

    def test_perform_store(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        context.request.action = GARequest.ACTION_CREATE

        def mocked_create(self, resource, parent):
            context.object = 'did_create'

        with patch.object(FakeStorageController, 'create', autospec=True) as m:
            m.side_effect = mocked_create
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_create')

        context.request.action = GARequest.ACTION_UPDATE

        def mocked_update(self, resource):
            context.object = 'did_update'

        with patch.object(FakeStorageController, 'update', autospec=True) as m:
            m.side_effect = mocked_update
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_update')

        context.request.action = GARequest.ACTION_DELETE

        def mocked_delete(self, resource, cascade):
            context.object = 'did_delete'

        with patch.object(FakeStorageController, 'delete', autospec=True) as m:
            m.side_effect = mocked_delete
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_delete')

        context.request.action = GARequest.ACTION_ASSIGN

        def mocked_assign(self, resource_name, resources, parent):
            context.object = 'did_assign'

        with patch.object(FakeStorageController, 'assign', autospec=True) as m:
            m.side_effect = mocked_assign
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_assign')

        with patch.object(FakeStorageController, 'assign', return_value='fake'):
            operations_controller._perform_store()
            self.assertEquals(len(context.errors), 1)

        with patch.object(FakeStorageController, 'assign', return_value=['fake', 'fake']):
            operations_controller._perform_store()
            self.assertEquals(len(context.errors), 3)

    def test_perform_push(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.parent_object = tstdk.GAEnterprise(name='parent')
        context.object = tstdk.GAEnterprise(name='object')

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        context.request.action = GARequest.ACTION_ASSIGN
        operations_controller._perform_push()
        self.assertEquals(context.events[0].entity.name, 'parent')
        self.assertEquals(context.events[0].action, GARequest.ACTION_UPDATE)
        context.clear_events()

        context.request.action = GARequest.ACTION_CREATE
        operations_controller._perform_push()
        self.assertEquals(context.events[0].entity.name, 'object')
        self.assertEquals(context.events[0].action, GARequest.ACTION_CREATE)
        context.clear_events()

        context.request.action = GARequest.ACTION_UPDATE
        operations_controller._perform_push()
        self.assertEquals(context.events[0].entity.name, 'object')
        self.assertEquals(context.events[0].action, GARequest.ACTION_UPDATE)
        context.clear_events()

        context.request.action = GARequest.ACTION_DELETE
        operations_controller._perform_push()
        self.assertEquals(context.events[0].entity.name, 'object')
        self.assertEquals(context.events[0].action, GARequest.ACTION_DELETE)
        context.clear_events()

    def test_populate_context_for_create_with_resource(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.parent_object = tstdk.GAEnterprise(name='parent')
        context.object = tstdk.GAEnterprise(name='object')

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller._populate_context_for_create_with_resource(resource=GAResource(name='fake', value=None))
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
        context.clear_errors()

        request.content = {'name': 'the_enterprise'}
        with patch.object(FakeStorageController, 'instantiate', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_create_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(context.object.name, 'the_enterprise')

        request.content = {'name': None}
        with patch.object(FakeStorageController, 'instantiate', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_create_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_CONFLICT)

    def test_populate_context_for_update_with_resource(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.parent_object = tstdk.GAEnterprise(name='parent')
        context.object = tstdk.GAEnterprise(name='object')

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller._populate_context_for_update_with_resource(resource=GAResource(name='fake', value=None))
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
        context.clear_errors()

        request.content = {'name': 'the_enterprise'}
        with patch.object(FakeStorageController, 'get', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_update_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(context.object.name, 'the_enterprise')

        request.content = {'name': None}
        with patch.object(FakeStorageController, 'get', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_update_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_CONFLICT)

    def test_populate_context_for_delete_with_resource(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.parent_object = tstdk.GAEnterprise(name='parent')
        context.object = tstdk.GAEnterprise(name='object')

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller._populate_context_for_delete_with_resource(resource=GAResource(name='fake', value=None))
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
        context.clear_errors()

        with patch.object(FakeStorageController, 'get', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_delete_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(len(context.errors), 0)

    def test_populate_context_for_assign_with_resource(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.parent_object = tstdk.GAEnterprise(name='parent')
        context.object = tstdk.GAEnterprise(name='object')

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        context.request.content = ['1', '2', '3']

        operations_controller._populate_context_for_assign_with_resource(resource=GAResource(name='enterprise', value=None))
        self.assertEquals(len(context.errors), 3)
        self.assertEquals(len(context.objects), 0)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
        self.assertEquals(context.errors[1].type, GAError.TYPE_NOTFOUND)
        self.assertEquals(context.errors[2].type, GAError.TYPE_NOTFOUND)

        context.clear_errors()
        with patch.object(FakeStorageController, 'get', return_value=tstdk.GAEnterprise(name='test')):
            operations_controller._populate_context_for_assign_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(len(context.objects), 3)
            self.assertEquals(context.objects[0].name, 'test')
            self.assertEquals(context.objects[1].name, 'test')
            self.assertEquals(context.objects[2].name, 'test')

    def test_prepare_context_for_write_operation_with_errors(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        context.request.action = GARequest.ACTION_DELETE
        context.request.resources = [GAResource(name='enterprise', value=None)]
        operations_controller._prepare_context_for_write_operation()
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTALLOWED)
        context.clear_errors()

        context.request.action = GARequest.ACTION_UPDATE
        context.request.resources = [GAResource(name='enterprise', value=None)]
        operations_controller._prepare_context_for_write_operation()
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_NOTALLOWED)
        context.clear_errors()

    def test_prepare_context_for_write_operation_without_errors(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_create(self, resource):
            self.context.object = 'did_create'

        with patch.object(GAOperationsController, '_populate_context_for_create_with_resource', autospec=True) as m:
            m.side_effect = mocked_create
            context.request.action = GARequest.ACTION_CREATE
            context.request.resources = [GAResource(name='enterprise', value=None)]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_create')

        def mocked_update(self, resource):
            self.context.object = 'did_update'

        with patch.object(GAOperationsController, '_populate_context_for_update_with_resource', autospec=True) as m:
            m.side_effect = mocked_update
            context.request.action = GARequest.ACTION_UPDATE
            context.request.resources = [GAResource(name='enterprise', value='id')]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_update')

        def mocked_delete(self, resource):
            self.context.object = 'did_delete'

        with patch.object(GAOperationsController, '_populate_context_for_delete_with_resource', autospec=True) as m:
            m.side_effect = mocked_delete
            context.request.action = GARequest.ACTION_DELETE
            context.request.resources = [GAResource(name='enterprise', value='id')]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_delete')

        def mocked_assign(self, resource):
            self.context.object = 'did_assign'

        with patch.object(GAOperationsController, '_populate_context_for_assign_with_resource', autospec=True) as m:
            m.side_effect = mocked_assign
            context.request.action = GARequest.ACTION_ASSIGN
            context.request.resources = [GAResource(name='enterprise', value='id')]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_assign')

    def test_perform_write_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            operations_controller._perform_write_operation()
            self.assertEquals(context.performed_delegates, ['begin_write_operation', 'check_perform_write', 'preprocess_write', 'did_perform_write', 'end_write_operation'])

    def test_perform_write_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

            context.performed_delegates = []
            context.add_error('fake')
            operations_controller._perform_write_operation()
            self.assertEquals(context.performed_delegates, [])

    def test_perform_write_operation_with_errors_in_the_middle1(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_write_operation()
                self.assertEquals(context.performed_delegates, ['begin_write_operation', 'check_perform_write'])

    def test_perform_write_operation_with_errors_in_the_middle2(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):

            if delegate == 'preprocess_write':
                context.add_error('fake')

            context.performed_delegates.append(delegate)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_write_operation()
                self.assertEquals(context.performed_delegates, ['begin_write_operation', 'check_perform_write', 'preprocess_write'])
