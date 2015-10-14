# -*- coding: utf-8 -*-

from mock import patch

from garuda.core.models import GASession
from garuda.plugins.default_authentication_plugin import DefaultAuthenticationPlugin
from garuda.tests.unit.sessions import GASessionsControllerTestCase


class TestFlushSession(GASessionsControllerTestCase):
    """
    """

    def setUp(self):
        """Initialize context

        """
        pass

    def tearDown(self):
        """ Cleanup context

        """
        pass

    def test_flush_all_sessions(self):
        """ Flush all sessions should succeed

        """
        garuda_uuid = self.get_valid_garuda_uuid()
        user = self.get_default_user()

        plugin = DefaultAuthenticationPlugin()
        self.sessions_controller.register_plugin(plugin)

        with patch.object(plugin, 'authenticate', return_value=user):
            session1 = self.create_session(request='Session1', garuda_uuid=garuda_uuid, is_listening_push_notifications=True)
            session2 = self.create_session(request='Session2', garuda_uuid=garuda_uuid, is_listening_push_notifications=True)
            session3 = self.create_session(request='Session3', garuda_uuid=garuda_uuid, is_listening_push_notifications=True)

        self.flush_sessions()
        self.assertNoSessionsForGaruda(garuda_uuid)
