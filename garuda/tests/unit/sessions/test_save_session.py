# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.controllers import AuthenticationController
from garuda.tests.unit.sessions import SessionsManagerTestCase


class TestSaveSession(SessionsManagerTestCase):
    """
    """

    def setUp(self):
        """ Initialize context

        """
        user = self.get_default_user()

        with patch.object(AuthenticationController, 'authenticate', return_value=user):
            self.session = self.create_session()

    def tearDown(self):
        """ Cleanup context

        """
        self.flush_sessions()

    def test_save_session_with_is_listening_push_notifications(self):
        """ Save session with is_listening_push_notifications should succeed

        """
        self.session.is_listening_push_notifications = True
        self.assertEquals(self.save_session(self.session), True)

        self.session = self.get_session(self.session.uuid)
        self.assertEquals(self.session.is_listening_push_notifications, True)
