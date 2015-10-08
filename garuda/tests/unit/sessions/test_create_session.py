# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.models import GASession
from garuda.core.controllers import GAAuthenticationController
from garuda.tests.unit.sessions import GASessionsManagerTestCase


class TestGetSession(GASessionsManagerTestCase):
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
        user = self.get_default_user()

        with patch.object(GAAuthenticationController, 'authenticate', return_value=user) as mock_method:
            session = self.create_session(request='A request', garuda_uuid=garuda_uuid)

        mock_method.assert_called_with(request='A request')
        self.assertEquals(len(session.uuid), 36)
        self.assertEquals(session.garuda_uuid, garuda_uuid)
        self.assertEquals(session.is_listening_push_notifications, False)
        self.assertEquals(session.user.to_dict(), user.to_dict())

    def test_create_session_without_authentication(self):
        """ Create a session with authentication failure should succeed

        """
        garuda_uuid = self.get_valid_garuda_uuid()
        user = self.get_default_user()
        user.api_key = None

        with patch.object(GAAuthenticationController, 'authenticate', return_value=user) as mock_method:
            session = self.create_session(request='A request', garuda_uuid=garuda_uuid)

        self.assertEquals(session, None)
