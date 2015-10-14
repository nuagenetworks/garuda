# -*- coding: utf-8 -*-

from mock import patch

from garuda.plugins.default_authentication_plugin import DefaultAuthenticationPlugin
from garuda.tests.unit.sessions import GASessionsControllerTestCase


class TestSaveSession(GASessionsControllerTestCase):
    """
    """

    def setUp(self):
        """ Initialize context

        """
        self.session = self.create_session()

    def tearDown(self):
        """ Cleanup context

        """
        self.flush_sessions()

    def test_save_session_with_is_listening_push_notifications(self):
        """ Save session with is_listening_push_notifications should succeed

        """
        self.sessions_controller.set_session_listening_status(self.session, True)
        self.assertEquals(self.get_session(self.session.uuid).is_listening_push_notifications, True)

        self.sessions_controller.set_session_listening_status(self.session, False)
        self.assertEquals(self.get_session(self.session.uuid).is_listening_push_notifications, False)
