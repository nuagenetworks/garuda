# -*- coding: utf-8 -*-
import redis
from uuid import uuid4
from unittest import TestCase

from garuda.core.lib import GASDKLibrary
from garuda.core.controllers import GAPermissionsController, GACoreController
from garuda.core.plugins import GAPermissionsPlugin
from garuda.plugins.storage import GAMongoStoragePlugin

import tests.tstdk.v1_0 as tstdk


class TestPermissionsController(TestCase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """
        Model:

        e1  --- u1  --- a1
            +-- u2  --- a2
            +-- u3

        e2  --- u4  --- a3
            +-- u5  --- a4
                    --- a5

        will be testing diverse permissions on that model for self.e0
        """
        GASDKLibrary().register_sdk('default', tstdk)

        cls.mongo_plugin = GAMongoStoragePlugin(db_name='permissions_test', sdk_identifier='default')
        cls.core_controller = GACoreController(garuda_uuid='test-garuda',
                                               redis_info={'host': '127.0.0.1', 'port': '6379', 'db': 7},
                                               storage_plugins=[cls.mongo_plugin])

        cls.storage_controller = cls.core_controller.storage_controller

        cls.core_controller.redis.flushall()

        cls.core_controller.start()
        cls.permissions_controller = cls.core_controller.permissions_controller

        cls.e0 = tstdk.GAEnterprise(username='e0')
        cls.storage_controller.create(resource=cls.e0, parent=None)

        cls.e1 = tstdk.GAEnterprise(name='e1')
        cls.e2 = tstdk.GAEnterprise(name='e2')

        cls.u1 = tstdk.GAUser(username='u1')
        cls.u2 = tstdk.GAUser(username='u2')
        cls.u3 = tstdk.GAUser(username='u3')
        cls.u4 = tstdk.GAUser(username='u4')
        cls.u5 = tstdk.GAUser(username='u5')

        cls.a1 = tstdk.GAUser(street='a1')
        cls.a2 = tstdk.GAUser(street='a2')
        cls.a3 = tstdk.GAUser(street='a3')
        cls.a4 = tstdk.GAUser(street='a4')
        cls.a5 = tstdk.GAUser(street='a5')

        cls.storage_controller.create(resource=cls.e1, parent=None)
        cls.storage_controller.create(resource=cls.u1, parent=cls.e1)
        cls.storage_controller.create(resource=cls.u2, parent=cls.e1)
        cls.storage_controller.create(resource=cls.u3, parent=cls.e1)
        cls.storage_controller.create(resource=cls.a1, parent=cls.u1)
        cls.storage_controller.create(resource=cls.a2, parent=cls.u2)

        cls.storage_controller.create(resource=cls.e2, parent=None)
        cls.storage_controller.create(resource=cls.u4, parent=cls.e2)
        cls.storage_controller.create(resource=cls.u5, parent=cls.e2)
        cls.storage_controller.create(resource=cls.a3, parent=cls.u4)
        cls.storage_controller.create(resource=cls.a4, parent=cls.u5)
        cls.storage_controller.create(resource=cls.a5, parent=cls.u5)

    @classmethod
    def tearDownClass(cls):
        """
        """
        cls.core_controller.redis.flushall()
        cls.core_controller.stop()
        cls.mongo_plugin.mongo.drop_database('permissions_test')

    def _assertHasPermission(self, target, permission):
        """
        """
        self.assertTrue(self.permissions_controller.has_permission(resource=self.e0, target=target, permission=permission))

    def _assertHasNotPermission(self, target, permission):
        """
        """
        self.assertFalse(self.permissions_controller.has_permission(resource=self.e0, target=target, permission=permission))

    def _assertNoPermission(self):
        """
        """
        self.assertTrue(self.permissions_controller.is_empty())

    def test_identifier(self):
        """
        """
        self.assertEquals(self.permissions_controller.identifier(), 'garuda.controller.permissions')
        self.assertEquals(self.permissions_controller.__class__.identifier(), 'garuda.controller.permissions')

    def test_managed_plugin_type(self):
        """
        """
        self.assertEquals(self.permissions_controller.managed_plugin_type(), GAPermissionsPlugin)
        self.assertEquals(self.permissions_controller.__class__.managed_plugin_type(), GAPermissionsPlugin)

    def test_compute_permission_redis_key(self):
        """
        """
        target = tstdk.GAUser(username='test')
        target.id = 'uid'

        parent = tstdk.GAEnterprise(name='ent')
        parent.id = 'pid'

        key = self.permissions_controller._compute_permission_redis_key()
        self.assertEquals(key, 'permission:*:*:*:*:*:*:*:*')

        key = self.permissions_controller._compute_permission_redis_key(permission_id='pid', resource_id='rid', target_type=target.rest_name, target_id=target.id, target_parent_type=parent.rest_name, target_parent_id=parent.id, scope='E')
        self.assertEquals(key, 'permission:pid:*:rid:user:uid:enterprise:pid:E')

        key = self.permissions_controller._compute_permission_redis_key(permission_id='pid', resource_id='rid', target_type=target.rest_name, target_id=target.id, target_parent_type=parent.rest_name, target_parent_id=parent.id, scope='I')
        self.assertEquals(key, 'permission:pid:*:rid:user:uid:enterprise:pid:I')

        key = self.permissions_controller._compute_permission_redis_key(permission_id='pid', resource_id='rid', target_type=target.rest_name, target_id=target.id, target_parent_type=parent.rest_name, target_parent_id=parent.id, scope='I', parent_permission_id='ppid')
        self.assertEquals(key, 'permission:pid:ppid:rid:user:uid:enterprise:pid:I')

    def test_root_level_permissions(self):
        """
        """
        self._assertNoPermission()
        self._assertHasNotPermission(target=self.e1, permission='read')

        self.permissions_controller.create_permission(resource=self.e0, target=self.e1, permission='read')

        self._assertHasPermission(target=self.e1, permission='read')

        self.permissions_controller.remove_permission(resource=self.e0, target=self.e1, permission='read')

        self._assertHasNotPermission(target=self.e1, permission='read')
        self._assertNoPermission()

    def test_second_level_permissions(self):
        """
        """
        self._assertNoPermission()

        self._assertHasNotPermission(target=self.e1, permission='read')
        self._assertHasNotPermission(target=self.u1, permission='write')
        self._assertHasNotPermission(target=self.u1, permission='read')

        self.permissions_controller.create_permission(resource=self.e0, target=self.u1, permission='write')

        self._assertHasPermission(target=self.e1, permission='read')
        self._assertHasPermission(target=self.u1, permission='write')

        self.permissions_controller.remove_permission(resource=self.e0, target=self.u1, permission='write')

        self._assertHasNotPermission(target=self.e1, permission='read')
        self._assertHasNotPermission(target=self.u1, permission='write')
        self._assertHasNotPermission(target=self.u1, permission='read')

        self._assertNoPermission()

    def test_remove_write_permission_at_object_level(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.a1, 'write')
        self.permissions_controller.remove_permission(self.e0, self.a1, 'write')

        self._assertNoPermission()

    def test_remove_multiple_permissions(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.a1, 'write')
        self.permissions_controller.create_permission(self.e0, self.a2, 'use')
        self.permissions_controller.create_permission(self.e0, self.u1, 'all')
        self.permissions_controller.create_permission(self.e0, self.e2, 'write')

        self.permissions_controller.remove_permission(self.e0, self.a1, 'write')
        self.permissions_controller.remove_permission(self.e0, self.a2, 'use')
        self.permissions_controller.remove_permission(self.e0, self.u1, 'all')
        self.permissions_controller.remove_permission(self.e0, self.e2, 'write')

        self._assertNoPermission()

    def test_permissions_bottom_computation(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.e1, 'use')

        self._assertHasPermission(self.u1, 'use')
        self._assertHasPermission(self.u2, 'use')
        self._assertHasPermission(self.u3, 'use')
        self._assertHasPermission(self.a1, 'use')
        self._assertHasPermission(self.a2, 'use')

        self._assertHasPermission(self.u1, 'read')
        self._assertHasPermission(self.u2, 'read')
        self._assertHasPermission(self.u3, 'read')
        self._assertHasPermission(self.a1, 'read')
        self._assertHasPermission(self.a2, 'read')

        self._assertHasNotPermission(self.u1, 'write')
        self._assertHasNotPermission(self.u2, 'write')
        self._assertHasNotPermission(self.u3, 'write')
        self._assertHasNotPermission(self.a1, 'write')
        self._assertHasNotPermission(self.a2, 'write')

        self.permissions_controller.remove_permission(self.e0, self.e1, 'use')

        self._assertNoPermission()

    def test_permissions_top_propagation(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.a1, 'use')

        self._assertHasPermission(target=self.a1, permission='use')
        self._assertHasPermission(target=self.u1, permission='read')
        self._assertHasPermission(target=self.e1, permission='read')
        self._assertHasNotPermission(target=self.e1, permission='use')
        self._assertHasNotPermission(target=self.u1, permission='use')

        self._assertHasNotPermission(target=self.u2, permission='read')
        self._assertHasNotPermission(target=self.u3, permission='read')
        self._assertHasNotPermission(target=self.a2, permission='read')

        self.permissions_controller.remove_permission(self.e0, self.a1, 'use')

        self._assertNoPermission()

    def test_create_read_permission_at_object_level(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.e1, 'read')

        self._assertHasPermission(self.u1, 'read')
        self._assertHasPermission(self.u2, 'read')
        self._assertHasPermission(self.u3, 'read')
        self._assertHasPermission(self.a1, 'read')
        self._assertHasPermission(self.a2, 'read')

        self.permissions_controller.create_permission(self.e0, self.e1, 'write')

        self._assertHasPermission(self.u1, 'write')
        self._assertHasPermission(self.u2, 'write')
        self._assertHasPermission(self.u3, 'write')
        self._assertHasPermission(self.a1, 'write')
        self._assertHasPermission(self.a2, 'write')
        self._assertHasPermission(self.u1, 'use')
        self._assertHasPermission(self.u2, 'use')
        self._assertHasPermission(self.u3, 'use')
        self._assertHasPermission(self.a1, 'use')
        self._assertHasPermission(self.a2, 'use')

        self.permissions_controller.remove_permission(self.e0, self.e1, 'write')

        self._assertHasPermission(self.u1, 'read')
        self._assertHasPermission(self.u2, 'read')
        self._assertHasPermission(self.u3, 'read')
        self._assertHasPermission(self.a1, 'read')
        self._assertHasPermission(self.a2, 'read')

        self._assertHasNotPermission(self.u1, 'write')
        self._assertHasNotPermission(self.u2, 'write')
        self._assertHasNotPermission(self.u3, 'write')
        self._assertHasNotPermission(self.a1, 'write')
        self._assertHasNotPermission(self.a2, 'write')
        self._assertHasNotPermission(self.u1, 'use')
        self._assertHasNotPermission(self.u2, 'use')
        self._assertHasNotPermission(self.u3, 'use')
        self._assertHasNotPermission(self.a1, 'use')
        self._assertHasNotPermission(self.a2, 'use')

        self.permissions_controller.remove_permission(self.e0, self.e1, 'read')

        self._assertHasNotPermission(self.u1, 'read')
        self._assertHasNotPermission(self.u2, 'read')
        self._assertHasNotPermission(self.u3, 'read')
        self._assertHasNotPermission(self.a1, 'read')
        self._assertHasNotPermission(self.a2, 'read')

        self._assertNoPermission()

    def test_override_write_permission_before_object(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.a1, 'use')
        self.permissions_controller.create_permission(self.e0, self.u1, 'write')

        self._assertHasPermission(self.u1, 'write')
        self._assertHasPermission(self.a1, 'write')
        self._assertHasNotPermission(self.e1, 'write')
        self._assertHasPermission(self.e1, 'read')

        self.permissions_controller.remove_permission(self.e0, self.a1, 'use')
        self.permissions_controller.remove_permission(self.e0, self.u1, 'write')

        self._assertNoPermission()

    def test_override_write_permission_after_object(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.e1, 'use')
        self.permissions_controller.create_permission(self.e0, self.u1, 'write')

        self._assertHasPermission(self.e1, 'read')
        self._assertHasPermission(self.e1, 'use')
        self._assertHasNotPermission(self.e1, 'write')

        self._assertHasPermission(self.u2, 'read')
        self._assertHasPermission(self.u2, 'use')
        self._assertHasNotPermission(self.u2, 'write')

        self._assertHasPermission(self.u1, 'read')
        self._assertHasPermission(self.u1, 'use')
        self._assertHasPermission(self.u1, 'write')

        self._assertHasPermission(self.a1, 'read')
        self._assertHasPermission(self.a1, 'use')
        self._assertHasPermission(self.a1, 'write')

        self._assertHasPermission(self.a2, 'read')
        self._assertHasPermission(self.a2, 'use')
        self._assertHasNotPermission(self.a2, 'write')

        self.permissions_controller.remove_permission(self.e0, self.e1, 'use')
        self.permissions_controller.remove_permission(self.e0, self.u1, 'write')

        self._assertNoPermission()

    def test_create_same_permission_twice(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.e1, 'read')
        self.permissions_controller.create_permission(self.e0, self.e1, 'read')

        self._assertHasPermission(self.e1, 'read')

        self.permissions_controller.remove_permission(self.e0, self.e1, 'read')

        self._assertHasNotPermission(self.e1, 'read')

        self._assertNoPermission()

    def test_remove_all_permissions_of_resource(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.e0, self.e1, 'read')
        self.permissions_controller.create_permission(self.e0, self.u1, 'read')
        self.permissions_controller.create_permission(self.e0, self.u4, 'write')
        self.permissions_controller.create_permission(self.e0, self.a3, 'use')

        self.permissions_controller.remove_all_permissions_of_resource(resource=self.e0)

        self._assertNoPermission()

    def test_remove_all_permissions_for_target(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(self.u1, self.e2, 'read')
        self.permissions_controller.create_permission(self.u2, self.e2, 'read')
        self.permissions_controller.create_permission(self.u3, self.e2, 'write')
        self.permissions_controller.create_permission(self.a1, self.e2, 'use')
        self.permissions_controller.create_permission(self.e1, self.e2, 'use')

        self.permissions_controller.remove_all_permissions_for_target(target=self.e2)

        self._assertNoPermission()

    def test_child_resource_ids_with_permission(self):
        """
        """
        self._assertNoPermission()

        self.permissions_controller.create_permission(resource=self.e0, target=self.u1, permission='read')
        self.permissions_controller.create_permission(resource=self.e0, target=self.u2, permission='read')
        self.permissions_controller.create_permission(resource=self.e0, target=self.u3, permission='write')

        ids = self.permissions_controller.child_resource_ids_with_permission(resource=self.e0, parent_id=self.e1.id, children_type='user', permission=None)
        self.assertEquals(ids, {self.u1.id, self.u2.id, self.u3.id})

        ids = self.permissions_controller.child_resource_ids_with_permission(resource=self.e0, parent_id=self.e1.id, children_type='user', permission='write')
        self.assertEquals(ids, {self.u3.id})

        self.permissions_controller.remove_all_permissions_of_resource(resource=self.e0)

        self._assertNoPermission()
