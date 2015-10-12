# -*- coding:utf-8 -*-

import redis

from garuda.core.controllers import GASessionsController
from garuda.tests import UnitTestCase
from bambou import NURESTRootObject


class GASessionsControllerTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        """
        super(GASessionsControllerTestCase, self).__init__(name)

        redis_connection = redis.StrictRedis(host='127.0.0.1', port='6379', db=0)
        self.session_controller = GASessionsController(plugins=[], core_controller=None, redis_conn=redis_connection)

    def get_valid_garuda_uuid(self):
        """
        """
        return "GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA"

    def create_session(self, request=None, garuda_uuid=None, is_listening_push_notifications=False):
        """
        """
        if garuda_uuid is None:
            garuda_uuid = self.get_valid_garuda_uuid()

        session = self.session_controller.create_session(request=request, garuda_uuid=garuda_uuid)

        if is_listening_push_notifications:
            session.is_listening_push_notifications = True
            self.save_session(session)

        return session

    def save_session(self, session):
        """
        """
        return self.session_controller.save(session)

    def flush_sessions(self, garuda_uuid=None):
        """
        """
        if garuda_uuid is None:
            garuda_uuid = self.get_valid_garuda_uuid()

        self.session_controller.flush_garuda(self.get_valid_garuda_uuid())

    def get_session(self, session_uuid):
        """
        """
        return self.session_controller.get_session(session_uuid)

    def get_default_user(self):
        """
        """
        root = NURESTRootObject()
        root.id = "bbbbbbbb-f93e-437d-b97e-4c945904e7bb"
        root.api_key = "aaaaaaaa-98d4-4c2b-a136-770c9cbf7cdc"
        root.user_name = "Test"
        return root

    def assertNoSessionsForGaruda(self, garuda_uuid):
        """
        """
        self.assertEquals(len(self.session_controller.get_all_sessions(garuda_uuid=garuda_uuid)), 0)
