# -*- coding: utf-8 -*-
from unittest import TestCase

from garuda.plugins.authentication import GASimpleAuthenticationPlugin
from garuda.core.models import GASession, GARequest, GAResource
from garuda.core.lib import GASDKLibrary

import tests.tstdk.v1_0 as tstdk


class FakeCoreController(object):

    def __init__(self):

        self.storage_controller = 'fake_storage_controller'


class TestSimpleAuthPlugin(TestCase):
    """
    """

    def test_identifiers(self):
        """
        """
        auth_plugin = GASimpleAuthenticationPlugin()
        self.assertEquals(auth_plugin.__class__.manifest().identifier, 'garuda.plugin.authentication.simple')
        self.assertEquals(auth_plugin.manifest().identifier, 'garuda.plugin.authentication.simple')

    def test_should_manage(self):
        """
        """
        auth_plugin = GASimpleAuthenticationPlugin()
        self.assertTrue(auth_plugin.should_manage(request='fake'))

    def test_extract_session_identifier(self):
        """
        """
        request = GARequest(action=GARequest.ACTION_READ)
        request.token = 'token'

        auth_plugin = GASimpleAuthenticationPlugin()

        self.assertEquals(auth_plugin.extract_session_identifier(request=request), 'token')

    def test_authenticate_without_auth_function(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)

        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource('root', None)]
        request.token = 'token'
        session = GASession()
        auth_plugin = GASimpleAuthenticationPlugin()
        auth_info = auth_plugin.authenticate(request=request, session=session)

        self.assertEquals(auth_info.__class__, tstdk.GARoot)

    def test_authenticate_with_auth_function(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)

        o_request = GARequest(action=GARequest.ACTION_READ)
        o_request.resources = [GAResource('root', None)]
        o_request.token = 'token'
        o_session = GASession()

        def auth_function(request, session, root_object_class, storage_controller):
            self.assertEquals(request, o_request)
            self.assertEquals(session, o_session)
            self.assertEquals(root_object_class, tstdk.GARoot)
            self.assertEquals(storage_controller, 'fake_storage_controller')

        auth_plugin = GASimpleAuthenticationPlugin()
        auth_plugin.core_controller = FakeCoreController()
        auth_plugin._auth_function = auth_function
        auth_plugin.authenticate(request=o_request, session=o_session)

    def test_authenticate_with_wrong_access(self):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)

        request = GARequest(action=GARequest.ACTION_READ)
        request.resources = [GAResource('note-good', None)]
        request.token = 'token'
        session = GASession()
        auth_plugin = GASimpleAuthenticationPlugin()
        auth_info = auth_plugin.authenticate(request=request, session=session)

        self.assertIsNone(auth_info)
