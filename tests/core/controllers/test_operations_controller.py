# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from bambou import NURESTRootObject

from garuda.core.controllers import GAOperationsController
from garuda.core.models import GAContext, GASession, GARequest, GAResource, GAError, GAStoragePluginQueryResponse

import tests.tstdk.v1_0 as tstdk


class FakeLogicController(object):
    """
    """

    def perform_delegate(self, delegate, context):
        """
        """
        context.performed_delegates.append(delegate)


class FakeStorageController(object):
    """
    """
    def instantiate(self, resource_name):
        """
        """
        pass

    def get(self, user_identifier, resource_name, identifier):
        """
        """
        return GAStoragePluginQueryResponse()

    def get_all(self, user_identifier, parent, resource_name, page, page_size, filter, order_by):
        """
        """
        return GAStoragePluginQueryResponse()

    def count(self, user_identifier, parent, resource_name, filter):
        """
        """
        return GAStoragePluginQueryResponse()

    def create(self, user_identifier, resource, parent):
        """
        """
        return GAStoragePluginQueryResponse()

    def update(self, user_identifier, resource):
        """
        """
        return GAStoragePluginQueryResponse()

    def delete(self, user_identifier, resource, cascade):
        """
        """
        return GAStoragePluginQueryResponse()

    def assign(self, user_identifier, resource_name, resources, parent):
        """
        """
        return GAStoragePluginQueryResponse()


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

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAUser(username='test'))):
            operations_controller._populate_parent_object_if_needed()

        self.assertEquals(context.parent_object.username, 'test')
        self.assertEquals(context.parent_object.rest_name, 'user')

    def test_populate_parent_object_if_needed_with_error(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        context = GAContext(session=session, request=request)

        enterprise1 = tstdk.GAEnterprise(name='enterprise1')
        enterprise1.parent_type = 'fake'
        enterprise1.parent_id = 'fake'
        context.object = enterprise1

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_error(error_type='error', title='', description='')):
            operations_controller._populate_parent_object_if_needed()
            self.assertEquals(len(context.errors), 1)

    def test_run_with_unknown_parent(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action='not-good')
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_NOTFOUND, title='', description='')):
            operations_controller.run()
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)

    def test_run_readall(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAEnterprise(name='enterprise1'))):

            def mocked_method(self, count_only):
                """ """
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
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_COUNT)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAEnterprise(name='enterprise1'))):

            def mocked_method(self, count_only):
                """ """
                assert count_only
                assert self.context.request.action == GARequest.ACTION_COUNT
                self.context.object = 'did_read_all_with_count'
                return GAStoragePluginQueryResponse()

            with patch.object(GAOperationsController, '_perform_readall_operation', autospec=True) as m:
                m.side_effect = mocked_method
                operations_controller.run()
                self.assertEquals(context.object, 'did_read_all_with_count')

    def test_read(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                """ """
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
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                """ """
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
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                """ """
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
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_DELETE)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                """ """
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
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action=GARequest.ACTION_ASSIGN)
        request.resources = [GAResource(name='enterprise', value='id')]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get', return_value=tstdk.GAEnterprise(name='enterprise1')):

            def mocked_method(self):
                """ """
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

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAUser(name='user1'))):

            operations_controller._prepare_context_for_read_operation()
            self.assertEquals(len(context.errors), 0)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_error(error_type='', title='', description='')):
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

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAUser(name='user1'))):
            operations_controller._perform_read_operation()
            self.assertEquals(context.performed_delegates, ['will_perform_read', 'did_perform_read'])

    def test_perform_read_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []
        context.object = 'obj'

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
            """ """
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(self.fake_storage_controller, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAUser(name='user1'))):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_read_operation()
                self.assertEquals(context.performed_delegates, ['will_perform_read'])

    def test_prepare_context_for_readall_operation(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(FakeStorageController, 'count', return_value=GAStoragePluginQueryResponse.init_with_data(data=None, count=42)):
            operations_controller._prepare_context_for_readall_operation(count_only=True)
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.total_count, 42)

        with patch.object(FakeStorageController, 'get_all', return_value=GAStoragePluginQueryResponse.init_with_data(data=[tstdk.GAUser(name='user1'), tstdk.GAUser(name='user2')], count=2)):
            operations_controller._prepare_context_for_readall_operation(count_only=False)
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(len(context.objects), 2)
            self.assertEquals(context.total_count, 2)

        with patch.object(FakeStorageController, 'get_all', return_value=GAStoragePluginQueryResponse.init_with_error(error_type='', title='', description='')):
            operations_controller._prepare_context_for_readall_operation(count_only=False)
            self.assertEquals(len(context.errors), 1)

        context.clear_errors()
        with patch.object(FakeStorageController, 'count', return_value=GAStoragePluginQueryResponse.init_with_error(error_type='', title='', description='')):
            operations_controller._prepare_context_for_readall_operation(count_only=True)
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

        with patch.object(self.fake_storage_controller, 'get_all', return_value=GAStoragePluginQueryResponse.init_with_data(data=[tstdk.GAUser(name='user1')], count=1)):
            operations_controller._perform_readall_operation(count_only=False)
            self.assertEquals(context.performed_delegates, ['will_perform_readall', 'did_perform_readall'])

    def test_perform_readall_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(self.fake_storage_controller, 'get_all', return_value=GAStoragePluginQueryResponse.init_with_data(data=[tstdk.GAUser(name='user1')], count=1)):
            context.performed_delegates = []
            context.add_error('fake')
            operations_controller._perform_readall_operation(count_only=False)
            self.assertEquals(context.performed_delegates, [])

    def test_perform_readall_operation_with_errors_in_the_middle1(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_READALL)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):
            """ """
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(self.fake_storage_controller, 'get_all', return_value=GAStoragePluginQueryResponse.init_with_data(data=[tstdk.GAUser(name='user1')], count=1)):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_readall_operation(count_only=False)
                self.assertEquals(context.performed_delegates, ['will_perform_readall'])

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

        def mocked_create(self, user_identifier, resource, parent):
            """ """
            context.object = 'did_create'
            return GAStoragePluginQueryResponse()

        with patch.object(FakeStorageController, 'create', autospec=True) as m:
            m.side_effect = mocked_create
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_create')

        context.request.action = GARequest.ACTION_UPDATE

        def mocked_update(self, user_identifier, resource):
            """ """
            context.object = 'did_update'
            return GAStoragePluginQueryResponse()

        with patch.object(FakeStorageController, 'update', autospec=True) as m:
            m.side_effect = mocked_update
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_update')

        context.request.action = GARequest.ACTION_DELETE

        def mocked_delete(self, user_identifier, resource, cascade):
            """ """
            context.object = 'did_delete'
            return GAStoragePluginQueryResponse()

        with patch.object(FakeStorageController, 'delete', autospec=True) as m:
            m.side_effect = mocked_delete
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_delete')

        context.request.action = GARequest.ACTION_ASSIGN

        def mocked_assign(self, user_identifier, resource_name, resources, parent):
            """ """
            context.object = 'did_assign'
            return GAStoragePluginQueryResponse()

        with patch.object(FakeStorageController, 'assign', autospec=True) as m:
            m.side_effect = mocked_assign
            operations_controller._perform_store()
            self.assertEquals(context.object, 'did_assign')

        with patch.object(FakeStorageController, 'assign', return_value=GAStoragePluginQueryResponse.init_with_error(error_type='fake', title='fake', description='fake')):
            operations_controller._perform_store()
            self.assertEquals(len(context.errors), 1)

        with patch.object(FakeStorageController, 'assign', return_value=GAStoragePluginQueryResponse.init_with_errors(['fake', 'fake'])):
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
        self.assertEquals(context.errors[0].type, GAError.TYPE_INVALID)
        context.clear_errors()

        request.content = {'name': 'the_enterprise'}
        with patch.object(FakeStorageController, 'instantiate', return_value=tstdk.GAEnterprise()):
            operations_controller._populate_context_for_create_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(context.object.name, 'the_enterprise')

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

        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse.init_with_error(error_type=GAError.TYPE_NOTFOUND, title='', description='')):
            operations_controller._populate_context_for_update_with_resource(resource=GAResource(name='fake', value=None))
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
            context.clear_errors()

        request.content = {'name': 'the_enterprise'}
        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse(data=tstdk.GAEnterprise())):
            operations_controller._populate_context_for_update_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(context.object.name, 'the_enterprise')

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

        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse.init_with_errors([GAError(type=GAError.TYPE_NOTFOUND, title='', description='')])):
            operations_controller._populate_context_for_delete_with_resource(resource=GAResource(name='fake', value=None))
            self.assertEquals(len(context.errors), 1)
            self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
            context.clear_errors()

        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAEnterprise())):
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

        context.clear_errors()
        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse.init_with_errors([GAError(type=GAError.TYPE_NOTFOUND, title='', description='', property_name='')])):
            operations_controller._populate_context_for_assign_with_resource(resource=GAResource(name='enterprise', value=None))
            self.assertEquals(len(context.errors), 3)
            self.assertEquals(len(context.objects), 0)
            self.assertEquals(context.errors[0].type, GAError.TYPE_NOTFOUND)
            self.assertEquals(context.errors[1].type, GAError.TYPE_NOTFOUND)
            self.assertEquals(context.errors[2].type, GAError.TYPE_NOTFOUND)

        context.clear_errors()
        with patch.object(FakeStorageController, 'get', return_value=GAStoragePluginQueryResponse.init_with_data(data=tstdk.GAEnterprise(name='test'))):
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
            """ """
            self.context.object = 'did_create'

        with patch.object(GAOperationsController, '_populate_context_for_create_with_resource', autospec=True) as m:
            m.side_effect = mocked_create
            context.request.action = GARequest.ACTION_CREATE
            context.request.resources = [GAResource(name='enterprise', value=None)]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_create')

        def mocked_update(self, resource):
            """ """
            self.context.object = 'did_update'

        with patch.object(GAOperationsController, '_populate_context_for_update_with_resource', autospec=True) as m:
            m.side_effect = mocked_update
            context.request.action = GARequest.ACTION_UPDATE
            context.request.resources = [GAResource(name='enterprise', value='id')]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_update')

        def mocked_delete(self, resource):
            """ """
            self.context.object = 'did_delete'

        with patch.object(GAOperationsController, '_populate_context_for_delete_with_resource', autospec=True) as m:
            m.side_effect = mocked_delete
            context.request.action = GARequest.ACTION_DELETE
            context.request.resources = [GAResource(name='enterprise', value='id')]
            operations_controller._prepare_context_for_write_operation()
            self.assertEquals(len(context.errors), 0)
            self.assertEquals(context.object, 'did_delete')

        def mocked_assign(self, resource):
            """ """
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
            self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_create', 'did_perform_create', 'did_perform_write'])

    def test_perform_write_operation_with_errors_right_away(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_CREATE)
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
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_method(self, delegate, context):
            """ """
            context.add_error('fake')
            context.performed_delegates.append(delegate)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as m:
                m.side_effect = mocked_method
                context.performed_delegates = []
                operations_controller._perform_write_operation()
                self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_create'])

    def test_perform_write_operation_with_errors_in_the_middle2(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        def mocked_perform_method(self, delegate, context):
            """ """
            context.performed_delegates.append(delegate)

        def mocked_store_method(self):
            """ """
            self.context.add_error('fake')

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            with patch.object(GAOperationsController, '_perform_store', autospec=True) as m:
                m.side_effect = mocked_store_method

                with patch.object(FakeLogicController, 'perform_delegate', autospec=True) as mm:
                    mm.side_effect = mocked_perform_method
                    context.performed_delegates = []
                    operations_controller._perform_write_operation()
                    self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_create'])

    def test_perform_update(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_UPDATE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=None):
            operations_controller._perform_write_operation()
            self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_update', 'did_perform_update', 'did_perform_write'])

    def test_perform_delete(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_DELETE)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=GAStoragePluginQueryResponse()):
            operations_controller._perform_write_operation()
            self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_delete', 'did_perform_delete', 'did_perform_write'])

    def test_perform_assign(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action=GARequest.ACTION_ASSIGN)
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        with patch.object(GAOperationsController, '_prepare_context_for_write_operation', return_value=GAStoragePluginQueryResponse()):
            operations_controller._perform_write_operation()
            self.assertEquals(context.performed_delegates, ['will_perform_write', 'will_perform_assign', 'did_perform_assign', 'did_perform_write'])

    def test_run_with_unknown_action(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        session.root_object = NURESTRootObject()
        session.root_object.id = 'test'
        request = GARequest(action='UKNOWN')
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller.run()
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_INVALID)

    def test_run_without_authenticated_session(self):
        """
        """
        session = GASession(garuda_uuid='xxx-xxx-xxx-xxx')
        request = GARequest(action='UKNOWN')
        request.resources = [GAResource(name='enterprise', value='id'), GAResource(name='user', value=None)]

        context = GAContext(session=session, request=request)
        context.performed_delegates = []

        operations_controller = GAOperationsController(context=context, logic_controller=self.fake_logic_controller, storage_controller=self.fake_storage_controller)

        operations_controller.run()
        self.assertEquals(len(context.errors), 1)
        self.assertEquals(context.errors[0].type, GAError.TYPE_AUTHENTICATIONFAILURE)
