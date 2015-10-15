# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.models import GASession
from garuda.plugins.default_authentication_plugin import DefaultAuthenticationPlugin
from garuda.tests.unit.sessions import GASessionsControllerTestCase


class TestRedisSession(GASessionsControllerTestCase):
    """
    """
    def setUp(self):
        """ Initialize context
        """
        self.sessions_controller.subscribe()

    def tearDown(self):
        """ Cleanup context
        """
        self.sessions_controller.unsubscribe()

    def test_simple_inserts(self):
        """
        """
        session = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())
        self.assertEquals(session.uuid, self.sessions_controller.get_session(session.uuid).uuid)

        self.sessions_controller.delete_session(session)
        self.assertEquals(self.sessions_controller.get_session(session.uuid), None)

    def test_local_sessions(self):
        """
        """
        not_session = GASession(garuda_uuid='not-garuda')

        session = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())
        self.assertIn(session.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions()])
        self.assertNotIn(session.uuid, [not_session.uuid for session in self.sessions_controller.get_all_local_sessions()])

    def test_flushing_local_sets_does_not_remove_sessions(self):
        """
        """
        session = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())

        self.sessions_controller.flush_local_sessions()

        self.assertIsNotNone(self.sessions_controller.get_session(session.uuid))

    def test_setting_session_listening_status(self):
        """
        """
        session = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())

        self.sessions_controller.set_session_listening_status(session, True)
        self.assertTrue(self.sessions_controller.get_session(session.uuid).is_listening_push_notifications)

        self.sessions_controller.set_session_listening_status(session, False)
        self.assertFalse(self.sessions_controller.get_session(session.uuid).is_listening_push_notifications)

    def test_getting_local_listening_sessions(self):
        """
        """
        session1 = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())
        session2 = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())
        session3 = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())

        self.sessions_controller.set_session_listening_status(session1, True)
        self.sessions_controller.set_session_listening_status(session2, True)

        self.assertIn(session1.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions(listening=True)])
        self.assertIn(session2.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions(listening=True)])
        self.assertNotIn(session3.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions(listening=True)])

    def test_expire_propagation(self):
        """
        """
        self.sessions_controller._default_session_ttl = 1
        session = self.create_session(request='A request', garuda_uuid=self.get_valid_garuda_uuid())

        self.sessions_controller.set_session_listening_status(session, True)

        self.assertIn(session.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions()])
        self.assertIn(session.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions(listening=True)])

        import time
        time.sleep(1.5)

        self.assertNotIn(session.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions()])
        self.assertNotIn(session.uuid, [session.uuid for session in self.sessions_controller.get_all_local_sessions(listening=True)])


