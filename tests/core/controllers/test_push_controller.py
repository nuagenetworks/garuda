# -*- coding: utf-8 -*-

from unittest import TestCase
from bambou import NURESTRootObject

from garuda.core.controllers import GACoreController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GAPluginManifest, GAPushEvent, GARequest

import tests.tstdk.v1_0 as tstdk


class FakeAuthPlugin(GAAuthenticationPlugin):

    @classmethod
    def manifest(self):
        return GAPluginManifest(name='test.fake.auth', version=1.0, identifier="test.fake.auth")

    def authenticate(self, request=None, session=None):
        root = NURESTRootObject()
        root.id = "bbbbbbbb-f93e-437d-b97e-4c945904e7bb"
        root.api_key = "aaaaaaaa-98d4-4c2b-a136-770c9cbf7cdc"
        root.user_name = "Test"
        return root

    def should_manage(self, request):
        return True

    def get_session_identifier(self, request):
        return request.token


class GAPushControllerTestCase(TestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        """
        """
        cls.fake_auth_plugin = FakeAuthPlugin()
        cls.core_controller = GACoreController(garuda_uuid='test-garuda',
                                               redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 6},
                                               authentication_plugins=[cls.fake_auth_plugin])

        cls.push_controller = cls.core_controller.push_controller
        cls.core_controller.sessions_controller._default_session_ttl = 3

    def setUp(self):
        """ Initialize context
        """
        self.core_controller.start()
        self.session = self.core_controller.sessions_controller.create_session(request='fake-request')
        self.session_event_queue_key = 'eventqueue:%s' % self.session.redis_key

    def tearDown(self):
        """ Cleanup context
        """
        self.core_controller.stop()

    def test_identifier(self):
        """
        """
        self.assertEquals(self.push_controller.identifier(), 'garuda.controller.push')
        self.assertEquals(self.push_controller.__class__.identifier(), 'garuda.controller.push')

    def test_push_event_creates_event_queue(self):
        """
        """
        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_CREATE, entity=entity)])

        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 1)
        self.assertFalse(self.push_controller.is_event_queue_empty(session=self.session))

    def test_events_gets_deleted_with_session_expiration(self):
        """
        """
        self.core_controller.sessions_controller._default_session_ttl = 1
        session = self.core_controller.sessions_controller.create_session(request='fake-request')

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_CREATE, entity=entity)])

        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 1)
        self.assertFalse(self.push_controller.is_event_queue_empty(session=self.session))

        import time
        time.sleep(1.5)

        self.assertEquals(self.push_controller.redis.llen('eventqueue:%s' % session.redis_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=session))

    def test_create_push(self):
        """
        """
        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_CREATE, entity=entity)])

        event = self.push_controller.get_next_event(session=self.session)

        self.assertIsNotNone(event)
        self.assertEquals(event.action, GARequest.ACTION_CREATE)
        self.assertEquals(entity.to_dict(), event.entity.to_dict())

    def test_update_push(self):
        """
        """
        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_UPDATE, entity=entity)])

        event = self.push_controller.get_next_event(session=self.session)

        self.assertIsNotNone(event)
        self.assertEquals(event.action, GARequest.ACTION_UPDATE)
        self.assertEquals(entity.to_dict(), event.entity.to_dict())

    def test_delete_push(self):
        """
        """
        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_DELETE, entity=entity)])

        event = self.push_controller.get_next_event(session=self.session)

        self.assertIsNotNone(event)
        self.assertEquals(event.action, GARequest.ACTION_DELETE)
        self.assertEquals(entity.to_dict(), event.entity.to_dict())

    def test_multiple_pushes(self):
        """
        """
        self.assertEquals(self.push_controller.redis.llen(self.session_event_queue_key), 0)
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

        entity = tstdk.GAEnterprise(name='name')
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_CREATE, entity=entity)])

        entity.name = 'modified'
        self.push_controller.push_events([GAPushEvent(action=GARequest.ACTION_UPDATE, entity=entity)])

        event1 = self.push_controller.get_next_event(session=self.session)

        self.assertIsNotNone(event1)
        self.assertEquals(event1.action, GARequest.ACTION_CREATE)
        self.assertEquals(event1.entity.name, 'name')
        self.assertFalse(self.push_controller.is_event_queue_empty(session=self.session))

        event2 = self.push_controller.get_next_event(session=self.session)

        self.assertIsNotNone(event2)
        self.assertEquals(event2.action, GARequest.ACTION_UPDATE)
        self.assertEquals(event2.entity.name, 'modified')
        self.assertTrue(self.push_controller.is_event_queue_empty(session=self.session))

    def test_next_event_timeout(self):
        """
        """
        event = self.push_controller.get_next_event(session=self.session, timeout=1)
        self.assertIsNone(event)
