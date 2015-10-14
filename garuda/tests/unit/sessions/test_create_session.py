# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.models import GASession
from garuda.plugins.default_authentication_plugin import DefaultAuthenticationPlugin
from garuda.tests.unit.sessions import GASessionsControllerTestCase


class TestGetSession(GASessionsControllerTestCase):
    """
    """
    def setUp(self):
        """ Initialize context
        """
        pass

    def tearDown(self):
        """ Cleanup context

        """
        self.flush_sessions()

    def test_create_session(self):
        """ Create a session with authentication success should succeed

        """
        garuda_uuid = self.get_valid_garuda_uuid()
        session = self.create_session(request='A request', garuda_uuid=garuda_uuid)

        self.assertEquals(len(session.uuid), 36)
        self.assertEquals(session.garuda_uuid, self.sessions_controller._garuda_uuid)
        self.assertEquals(session.is_listening_push_notifications, False)

    def test_create_session_without_authentication(self):
        """ Create a session with authentication failure should succeed

        """
        garuda_uuid = self.get_valid_garuda_uuid()

        with patch.object(self.fake_auth_plugin, 'authenticate', return_value=None) as mock_method:
            session = mock_method()

        self.assertEquals(session, None)
