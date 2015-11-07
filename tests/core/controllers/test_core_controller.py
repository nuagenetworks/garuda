# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch

from garuda.core.lib import GASDKLibrary
from garuda.core.controllers import GACoreController
from garuda.core.models import GASession, GARequest, GAController, GAResource, GAError, GAResponseFailure, GAResponseSuccess

import tests.tstdk.v1_0 as tstdk


class AdditionalController(GAController):

    def __init__(self, core_controller):
        """
        """
        super(AdditionalController, self).__init__(core_controller=core_controller)

        self.is_ready = False
        self.is_started = False

    def ready(self):
        self.is_ready = True

    def start(self):
        self.is_started = True

    def stop(self):
        self.is_started = False

    @classmethod
    def identifier(cls):
        """
        """
        return 'test.controller.additional'


class TestCoreController(TestCase):
    """
    """

    def test_identifiers(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        self.assertIsNotNone(core_controller.uuid)
        self.assertEquals(core_controller.garuda_uuid, 'test-garuda')

    def test_redis_information(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        self.assertIsNotNone(core_controller.redis)
        self.assertEquals(core_controller.redis_host, '127.0.0.1')
        self.assertEquals(core_controller.redis_port, 6379)
        self.assertEquals(core_controller.redis_db, 6)

    def test_controllers(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})
        self.assertIsNotNone(core_controller.storage_controller)
        self.assertIsNotNone(core_controller.logic_controller)
        self.assertIsNotNone(core_controller.push_controller)
        self.assertIsNotNone(core_controller.permissions_controller)
        self.assertIsNotNone(core_controller.sessions_controller)

    def test_additonal_controllers(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6})

        with self.assertRaises(KeyError):
            core_controller.additional_controller(identifier='nope')

        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6},
                                           additional_controller_classes=[AdditionalController])

        self.assertIsNotNone(core_controller.additional_controller(identifier='test.controller.additional'))

    def test_lifecycle(self):
        """
        """
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        additional = core_controller.additional_controller('test.controller.additional')

        self.assertTrue(additional.is_ready)

        core_controller.start()
        self.assertTrue(core_controller.running)
        self.assertTrue(additional.is_started)

        with self.assertRaises(RuntimeError):
            core_controller.start()

        core_controller.stop()
        self.assertFalse(core_controller.running)
        self.assertFalse(additional.is_started)

        with self.assertRaises(RuntimeError):
            core_controller.stop()

    def test_execute_model_request_with_invalid_session(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value=None)]

        with patch.object(core_controller.sessions_controller, 'get_session', return_value=None):
            with patch.object(core_controller.sessions_controller, 'get_session', return_value=None):
                result = core_controller.execute_model_request(request)
                self.assertEquals(result.__class__, GAResponseFailure)
                self.assertEquals(result.content[0].type, GAError.TYPE_UNAUTHORIZED)

    def test_execute_model_request_with_create_session(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='root', value=None)]

        with patch.object(core_controller.sessions_controller, 'get_session', return_value=None):
            with patch.object(core_controller.sessions_controller, 'create_session', return_value=GASession(garuda_uuid='test-garuda', root_object=tstdk.GARoot())):
                result = core_controller.execute_model_request(request)
                self.assertEquals(result.__class__, GAResponseSuccess)
                self.assertEquals(result.content[0].__class__, tstdk.GARoot)

    def test_execute_model_request_with_valid_session(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value=None)]

        with patch.object(core_controller.sessions_controller, 'get_session_identifier', return_value='token'):
            with patch.object(core_controller.sessions_controller, 'get_session', return_value=GASession(garuda_uuid='test-garuda', root_object=tstdk.GARoot())):
                result = core_controller.execute_model_request(request)
                self.assertEquals(result.__class__, GAResponseFailure)  # nothing exists that's fine

    def test_execute_event_request_with_invalid_session(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value=None)]

        with patch.object(core_controller.sessions_controller, 'get_session', return_value=None):
            result = core_controller.execute_events_request(request)
            self.assertEquals(result[0], None)
            self.assertEquals(result[1].__class__, GAResponseFailure)
            self.assertEquals(len(result[1].content), 1)
            self.assertEquals(result[1].content[0].type, GAError.TYPE_UNAUTHORIZED)

    def test_execute_event_request_with_valid_session(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': 6379, 'db': 6}, additional_controller_classes=[AdditionalController])
        request = GARequest(action=GARequest.ACTION_CREATE)
        request.resources = [GAResource(name='enterprise', value=None)]

        with patch.object(core_controller.sessions_controller, 'get_session', return_value=GASession(garuda_uuid='test-garuda')):
            result = core_controller.execute_events_request(request)
            self.assertEquals(result[0].__class__, GASession)
            self.assertEquals(result[1], None)
