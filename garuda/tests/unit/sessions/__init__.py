# -*- coding:utf-8 -*-

from garuda.core.controllers import SessionsManager
from garuda.tests import UnitTestCase
from bambou import NURESTRootObject


class SessionsManagerTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        """
        super(SessionsManagerTestCase, self).__init__(name)
        self.manager = SessionsManager(plugins=[])

    def get_valid_garuda_uuid(self):
        """
        """
        return "GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA"

    def create_session(self, request=None, garuda_uuid=None, is_listening_push_notifications=False):
        """
        """
        if garuda_uuid is None:
            garuda_uuid = self.get_valid_garuda_uuid()


        session = self.manager.create_session(request=request, garuda_uuid=garuda_uuid)

        if is_listening_push_notifications:
            session.is_listening_push_notifications = True
            self.save_session(session)

        return session

    def save_session(self, session):
        """
        """
        return self.manager.save(session)

    def flush_sessions(self, garuda_uuid=None):
        """
        """
        if garuda_uuid is None:
            garuda_uuid = self.get_valid_garuda_uuid()

        self.manager.flush_garuda(self.get_valid_garuda_uuid())

    def get_session(self, session_uuid):
        """
        """
        return self.manager.get(session_uuid)

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
        self.assertEquals(len(self.manager.get_all(garuda_uuid=garuda_uuid)), 0)
