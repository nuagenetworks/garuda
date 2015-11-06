# -*- coding: utf-8 -*-

import redis
from unittest import TestCase
from mock import patch

from garuda.channels.rest import GAFalconChannel
from garuda.plugins.authentication import GASimpleAuthenticationPlugin
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.core.controllers import GAChannelsController
from garuda.core.plugins import GAAuthenticationPlugin
from garuda.core.models import GAPluginManifest, GASession, GAPushEvent, GARequest, GAController

import tests.tstdk.v1_0 as tstdk

class TestChannelsController(TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """
        """
        def auth_function(request, session, root_object_class, storage_controller):
            pass

        cls.falcon_channel = GAFalconChannel(port=5454)
        cls.authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
        cls.storage_plugin = GAMongoStoragePlugin(db_name='test-db')
        cls.redis_info = {'host': '127.0.0.1', 'port': 6379, 'db': 6}

        cls.channels_controller = GAChannelsController(garuda_uuid='garuda-uuid',
                                                         channels=[cls.falcon_channel],
                                                         redis_info=cls.redis_info,
                                                         additional_controller_classes=[],
                                                         logic_plugins=[],
                                                         authentication_plugins=[cls.authentication_plugin],
                                                         storage_plugins=[cls.storage_plugin],
                                                         permission_plugins=[])
    def test_initialization(self):
        """
        """

        self.assertEquals(self.channels_controller.garuda_uuid, 'garuda-uuid')
        self.assertEquals(self.channels_controller.redis_info, self.redis_info)

        self.assertEquals(self.channels_controller.channels, [self.falcon_channel])
        self.assertEquals(self.channels_controller.logic_plugins, [])
        self.assertEquals(self.channels_controller.authentication_plugins, [self.authentication_plugin])
        self.assertEquals(self.channels_controller.storage_plugins, [self.storage_plugin])
        self.assertEquals(self.channels_controller.permission_plugins, [])
        self.assertEquals(self.channels_controller.additional_controller_classes, [])
        self.assertEquals(self.channels_controller.channel_pids, [])

    def test_lifecycle(self):
        """
        """
        self.channels_controller.start()

        self.assertEquals(len(self.channels_controller.channel_pids), 1)

        self.channels_controller.stop()

        self.assertEquals(len(self.channels_controller.channel_pids), 0)