# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.controllers import GAAuthenticationController
from garuda.tests.unit.sessions import GASessionsManagerTestCase


class TestGetSession(GASessionsManagerTestCase):
    """
    """

    def setUp(self):
        """ Initialize context
        """
        user = self.get_default_user()

        with patch.object(GAAuthenticationController, 'authenticate', return_value=user):
            self.session = self.create_session()

    def tearDown(self):
        """ Cleanup context
        """
        self.flush_sessions()

    def test_get_existing_session(self):
        """ Get a session with existing uuid should return the session

        """
        session = self.get_session(self.session.uuid)
        self.assertEquals(session.to_dict(), self.session.to_dict())

    def test_get_unknown_session(self):
        """ Get a session with unknown uuid should return None

        """
        session = self.get_session('0000-000-0000000-00000')
        self.assertEquals(session, None)