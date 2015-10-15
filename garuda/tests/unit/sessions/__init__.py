# -*- coding:utf-8 -*-

import redis

from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GAPluginManifest
from garuda.core.controllers import GASessionsController, GACoreController
from garuda.tests import UnitTestCase
from bambou import NURESTRootObject

class FakCoreController(object):

    @property
    def uuid(self): return 'GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA'

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
        """
        """
        return True

    def get_session_identifier(self, request):
        """
        """
        return request.token



class GASessionsControllerTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        """
        super(GASessionsControllerTestCase, self).__init__(name)

        redis_connection = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)

        self.fake_auth_plugin = FakeAuthPlugin()
        self.fake_core_controller = FakCoreController()

        self.sessions_controller = GASessionsController(plugins=[self.fake_auth_plugin], core_controller=self.fake_core_controller, redis_conn=redis_connection)

    def get_valid_garuda_uuid(self):
        """
        """
        return self.sessions_controller.core_controller.uuid

    def create_session(self, request=None, garuda_uuid=None, is_listening_push_notifications=False):
        """
        """
        return self.sessions_controller.create_session(request=request)

    def save_session(self, session):
        """
        """
        self.sessions_controller._save_session(session)
        return session

    def flush_sessions(self, garuda_uuid=None):
        """
        """
        self.sessions_controller.flush_local_sessions()

    def get_session(self, session_uuid):
        """
        """
        return self.sessions_controller.get_session(session_uuid)

    def get_default_user(self):
        """
        """
        return self.fake_auth_plugin.authenticate()

    def assertNoSessionsForGaruda(self, garuda_uuid):
        """
        """
        self.assertEquals(len(self.sessions_controller.get_all_local_sessions()), 0)
