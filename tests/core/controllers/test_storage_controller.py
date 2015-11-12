# -*- coding: utf-8 -*-
from unittest2 import TestCase
from mock import patch

from garuda.core.lib import GASDKLibrary
from garuda.core.models import GAPluginManifest
from garuda.core.controllers import GACoreController
from garuda.core.plugins import GAStoragePlugin

from tests.tstdk import v1_0 as tstdk


class FakeStoragePlugin(GAStoragePlugin):

    @classmethod
    def manifest(self):
        return GAPluginManifest(name='test.fake.storage', version=1.0, identifier='test.fake.storage')

    def instantiate(self):
        pass

    def get(self):
        pass

    def get_all(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def delete_multiple(self):
        pass

    def assign(self):
        pass

    def count(self):
        pass


class TestStorageController(TestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        """
        """
        GASDKLibrary().register_sdk('default', tstdk)
        cls.plugin = FakeStoragePlugin()
        cls.core_controller = GACoreController(garuda_uuid='test-garuda', redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 5}, storage_plugins=[cls.plugin])
        cls.storage_controller = cls.core_controller.storage_controller

    def test_identifier(self):
        """
        """
        self.assertEquals(self.storage_controller.identifier(), 'garuda.controller.storage')
        self.assertEquals(self.storage_controller.__class__.identifier(), 'garuda.controller.storage')

    def test_plugin_caching(self):
        """
        """
        self.assertEquals('fake' in self.storage_controller._managing_plugin_registry, False)

        managing_plugin = self.storage_controller._managing_plugin(resource_name='fake', identifier=None)
        self.assertEquals('fake' in self.storage_controller._managing_plugin_registry, True)
        self.assertEquals(managing_plugin, self.plugin)

        self.storage_controller.unregister_plugin(self.plugin)
        self.assertEquals('fake' in self.storage_controller._managing_plugin_registry, False)

        self.storage_controller.register_plugin(self.plugin)

    def test_instantiate(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'instantiate', return_value=tstdk.GAEnterprise()):
            self.assertEquals(self.storage_controller.instantiate(resource_name='test').rest_name, 'enterprise')

    def test_get(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'get', return_value=tstdk.GAEnterprise(name='enterprise')):
            self.assertEquals(self.storage_controller.get(user_identifier='owner_identifier', resource_name='test', identifier='id').name, 'enterprise')

    def test_get_all(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'get_all', return_value=[tstdk.GAEnterprise(name='enterprise1'), tstdk.GAEnterprise(name='enterprise2')]):
            result = self.storage_controller.get_all(user_identifier='owner_identifier', parent='parent', resource_name='test')
            self.assertEquals(len(result), 2)
            self.assertEquals(result[0].name, 'enterprise1')
            self.assertEquals(result[1].name, 'enterprise2')

    def test_create(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'create', return_value='ok'):
            self.assertEquals(self.storage_controller.create(user_identifier='owner_identifier', parent=tstdk.GAEnterprise(name='enterprise1'), resource=tstdk.GAEnterprise(name='enterprise2')), 'ok')

    def test_update(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'update', return_value='ok'):
            self.assertEquals(self.storage_controller.update(user_identifier='owner_identifier', resource=tstdk.GAEnterprise(name='enterprise1')), 'ok')

    def test_delete(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'delete', return_value='ok'):
            self.assertEquals(self.storage_controller.delete(user_identifier='owner_identifier', resource=tstdk.GAEnterprise(name='enterprise1'), cascade=True), 'ok')

    def test_delete_multiple(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'delete_multiple', return_value='ok'):
            self.assertEquals(self.storage_controller.delete_multiple(user_identifier='owner_identifier', resources=[tstdk.GAEnterprise(name='enterprise1')], cascade=True), 'ok')

    def test_assign(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'assign', return_value='ok'):
            self.assertEquals(self.storage_controller.assign(user_identifier='owner_identifier', resource_name=tstdk.GAEnterprise(name='enterprise1'), resources=[tstdk.GAEnterprise(name='enterprise2')], parent='parent'), 'ok')

    def test_count(self):
        """
        """
        with patch.object(FakeStoragePlugin, 'count', return_value='ok'):
            self.assertEquals(self.storage_controller.count(user_identifier='owner_identifier', parent='parent', resource_name='test'), 'ok')
