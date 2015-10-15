# -*- coding: utf-8 -*-

from bambou import NURESTRootObject
from garuda.core.models import GAPluginManifest, GASession
from garuda.core.plugins import GAAuthenticationPlugin

class FakeCoreController(object):

    @property
    def uuid(self):
        return 'GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA'

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