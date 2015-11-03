# -*- coding: utf-8 -*-

import redis
import pymongo
import bambou
from mock import patch

from garuda.core.lib import SDKLibrary
from garuda.tests import UnitTestCase
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.core.controllers import GAStorageController
import garuda.tests.tstdk.v1_0 as tstdk

class FakeCoreController(object):

    @property
    def uuid(self):
        return 'GGGGG-AAAAA-RRRRR-UUUU-DDDDD-AAAA'


class GAStorageControllerTestCase(UnitTestCase):
    """
    """
    def __init__(self, name):
        """
        """
        super(GAStorageControllerTestCase, self).__init__(name)
        self.mongo = pymongo.MongoClient('mongodb://127.0.0.1:27017')
        self.db = self.mongo['unit_test']

        SDKLibrary().register_sdk('default', tstdk)

        self.fake_core_controller = FakeCoreController()
        self.mongo_plugin = GAMongoStoragePlugin(db_name='unit_test')

        self.storage_controller = GAStorageController(plugins=[self.mongo_plugin], core_controller=self.fake_core_controller)
        self.storage_controller.ready()

    def setUp(self):
        """
        """
        self.storage_controller.start()

    def tearDown(self):
        """
        """
        self.storage_controller.stop()
        self.mongo.drop_database('unit_test')

    def test_instantiate_enterprise(self):
        """
        """
        obj = self.storage_controller.instantiate(resource_name=tstdk.GAEnterprise.rest_name)
        self.assertEquals(obj.__class__, tstdk.GAEnterprise)

    def test_create_enterprise(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')

        self.assertEquals(self.db.enterprise.count(), 0)
        self.storage_controller.create(resource=enterprise1, parent=None)
        self.assertEquals(self.db.enterprise.count(), 1)

    def test_get_enterprise_by_id(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        self.storage_controller.create(resource=enterprise1, parent=None)
        ret = self.storage_controller.get(resource_name=tstdk.GAEnterprise.rest_name, identifier=enterprise1.id)
        self.assertEquals(ret.id, enterprise1.id)
        self.assertEquals(ret.name, enterprise1.name)
        self.assertEquals(ret.description, enterprise1.description)

    def test_count_enterprises(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        enterprise3 = tstdk.GAEnterprise(name='enterprise 3', description='the enterprise 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=enterprise3, parent=None)

        ret = self.storage_controller.count(resource_name=tstdk.GAEnterprise.rest_name, parent=None)
        self.assertEquals(ret, 3)

    def test_get_all_enterprises(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        enterprise3 = tstdk.GAEnterprise(name='enterprise 3', description='the enterprise 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=enterprise3, parent=None)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAEnterprise.rest_name, parent=None)
        self.assertEquals(count, 3)
        self.assertEquals(len(ret), 3)

        self.assertEquals(ret[0].id, enterprise1.id)
        self.assertEquals(ret[0].name, enterprise1.name)
        self.assertEquals(ret[0].description, enterprise1.description)

        self.assertEquals(ret[1].id, enterprise2.id)
        self.assertEquals(ret[1].name, enterprise2.name)
        self.assertEquals(ret[1].description, enterprise2.description)

        self.assertEquals(ret[2].id, enterprise3.id)
        self.assertEquals(ret[2].name, enterprise3.name)
        self.assertEquals(ret[2].description, enterprise3.description)

    def test_get_all_enterprises_with_filter(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise', description='the enterprise')
        enterprise3 = tstdk.GAEnterprise(name='enterprise 3', description='the enterprise 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=enterprise3, parent=None)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAEnterprise.rest_name, parent=None, filter='name == enterprise')
        self.assertEquals(count, 1)
        self.assertEquals(len(ret), 1)

        self.assertEquals(ret[0].id, enterprise2.id)
        self.assertEquals(ret[0].name, enterprise2.name)
        self.assertEquals(ret[0].description, enterprise2.description)

    def test_update_enterprise(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        self.storage_controller.create(resource=enterprise1, parent=None)

        enterprise1.name = 'modified name'
        enterprise1.description = 'modified description'

        ret = self.storage_controller.get(resource_name=tstdk.GAEnterprise.rest_name, identifier=enterprise1.id)
        self.assertEquals(ret.id, enterprise1.id)
        self.assertNotEquals(ret.name, enterprise1.name)
        self.assertNotEquals(ret.description, enterprise1.description)

        self.storage_controller.update(resource=enterprise1)
        ret = self.storage_controller.get(resource_name=tstdk.GAEnterprise.rest_name, identifier=enterprise1.id)
        self.assertEquals(ret.id, enterprise1.id)
        self.assertEquals(ret.name, enterprise1.name)
        self.assertEquals(ret.description, enterprise1.description)

    def test_delete_enterprise(self):
        """ Test counting enterprises
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        self.storage_controller.create(resource=enterprise1, parent=None)

        count = self.storage_controller.count(resource_name=tstdk.GAEnterprise.rest_name, parent=None)
        self.assertEquals(count, 1)

        self.storage_controller.delete(resource=enterprise1)

        count = self.storage_controller.count(resource_name=tstdk.GAEnterprise.rest_name, parent=None)
        self.assertEquals(count, 0)

    def test_create_user(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        user1 = tstdk.GAUser(username='primalmotion', full_name='Antoine Mercadal')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)

        self.assertEquals(self.db.enterprise.count(), 2)
        self.assertEquals(self.db.user.count(), 1)

    def test_get_user_by_id(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        user1 = tstdk.GAUser(username='primalmotion', full_name='Antoine Mercadal')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)

        ret = self.storage_controller.get(resource_name=tstdk.GAUser.rest_name, identifier=user1.id)
        self.assertEquals(ret.id, user1.id)
        self.assertEquals(ret.username, user1.username)
        self.assertEquals(ret.full_name, user1.full_name)

    def test_count_users(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        enterprise3 = tstdk.GAEnterprise(name='enterprise 3', description='the enterprise 3')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=enterprise3, parent=None)

        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise2)

        ret = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(ret, 2)
        ret = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise2)
        self.assertEquals(ret, 1)
        ret = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise3)
        self.assertEquals(ret, 0)

    def test_get_all_users(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(count, 3)
        self.assertEquals(len(ret), 3)

        self.assertEquals(ret[0].id, user1.id)
        self.assertEquals(ret[0].username, user1.username)
        self.assertEquals(ret[0].full_name, user1.full_name)

        self.assertEquals(ret[1].id, user2.id)
        self.assertEquals(ret[1].username, user2.username)
        self.assertEquals(ret[1].full_name, user2.full_name)

        self.assertEquals(ret[2].id, user3.id)
        self.assertEquals(ret[2].username, user3.username)
        self.assertEquals(ret[2].full_name, user3.full_name)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=enterprise2)
        self.assertEquals(count, 0)
        self.assertEquals(len(ret), 0)

    def test_get_all_users_with_filter(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=enterprise1, filter='username == primalmotion2')
        self.assertEquals(count, 1)
        self.assertEquals(len(ret), 1)

        self.assertEquals(ret[0].id, user2.id)
        self.assertEquals(ret[0].username, user2.username)
        self.assertEquals(ret[0].full_name, user2.full_name)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=enterprise2, filter='username == primalmotion2')
        self.assertEquals(count, 0)
        self.assertEquals(len(ret), 0)

    def test_update_user(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)

        user1.username = 'modified username'
        user1.full_name = 'modified full_name'

        ret = self.storage_controller.get(resource_name=tstdk.GAUser.rest_name, identifier=user1.id)
        self.assertEquals(ret.id, user1.id)
        self.assertNotEquals(ret.username, user1.username)
        self.assertNotEquals(ret.full_name, user1.full_name)

        self.storage_controller.update(resource=user1)
        ret = self.storage_controller.get(resource_name=tstdk.GAUser.rest_name, identifier=user1.id)
        self.assertEquals(ret.id, user1.id)
        self.assertEquals(ret.username, user1.username)
        self.assertEquals(ret.full_name, user1.full_name)

    def test_delete_users(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(count, 1)

        self.storage_controller.delete(resource=user1)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(count, 0)

    def test_delete_enterprise_should_delete_users_and_addresses(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        enterprise2 = tstdk.GAEnterprise(name='enterprise 2', description='the enterprise 2')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')
        address1 = tstdk.GAAddress(street='rue gretry')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=enterprise2, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise2)
        self.storage_controller.create(resource=address1, parent=user1)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(count, 2)

        count = self.storage_controller.count(resource_name=tstdk.GAAddress.rest_name, parent=user1)
        self.assertEquals(count, 1)

        self.storage_controller.delete(resource=enterprise1)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise1)
        self.assertEquals(count, 0)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=enterprise2)
        self.assertEquals(count, 1)

        self.assertEquals(self.db.address.count(), 0)

    def test_assign_user(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        group1 = tstdk.GAGroup(name='group 1', description='the group 1')
        group2 = tstdk.GAGroup(name='group 2', description='the group 2')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=group1, parent=None)
        self.storage_controller.create(resource=group2, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group1)
        self.assertEquals(count, 0)

        count = self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group2)
        self.assertEquals(count, 0)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user1, user2], parent=group1)
        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user3], parent=group2)

        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group1), 2)
        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group2), 1)

    def test_get_all_assigned_users(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        group1 = tstdk.GAGroup(name='group 1', description='the group 1')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=group1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user1, user2, user3], parent=group1)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=group1)
        self.assertEquals(count, 3)

        self.assertEquals(ret[0].id, user1.id)
        self.assertEquals(ret[0].username, user1.username)
        self.assertEquals(ret[0].full_name, user1.full_name)

        self.assertEquals(ret[1].id, user2.id)
        self.assertEquals(ret[1].username, user2.username)
        self.assertEquals(ret[1].full_name, user2.full_name)

        self.assertEquals(ret[2].id, user3.id)
        self.assertEquals(ret[2].username, user3.username)
        self.assertEquals(ret[2].full_name, user3.full_name)

    def test_get_all_assigned_users_with_filter(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        group1 = tstdk.GAGroup(name='group 1', description='the group 1')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=group1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user1, user2, user3], parent=group1)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=group1, filter='username == primalmotion2')
        self.assertEquals(count, 1)

        self.assertEquals(ret[0].id, user2.id)
        self.assertEquals(ret[0].username, user2.username)
        self.assertEquals(ret[0].full_name, user2.full_name)

    def test_unassign_user(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        group1 = tstdk.GAGroup(name='group 1', description='the group 1')
        group2 = tstdk.GAGroup(name='group 2', description='the group 2')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=group1, parent=None)
        self.storage_controller.create(resource=group2, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user1, user2], parent=group1)
        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user3], parent=group2)
        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group1), 2)
        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group2), 1)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[], parent=group1)
        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[], parent=group2)
        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group1), 0)
        self.assertEquals(self.storage_controller.count(resource_name=tstdk.GAUser.rest_name, parent=group2), 0)

    def test_delete_user_remove_assignation(self):
        """
        """
        enterprise1 = tstdk.GAEnterprise(name='enterprise 1', description='the enterprise 1')
        group1 = tstdk.GAGroup(name='group 1', description='the group 1')
        user1 = tstdk.GAUser(username='primalmotion1', full_name='Antoine Mercadal 1')
        user2 = tstdk.GAUser(username='primalmotion2', full_name='Antoine Mercadal 2')
        user3 = tstdk.GAUser(username='primalmotion3', full_name='Antoine Mercadal 3')

        self.storage_controller.create(resource=enterprise1, parent=None)
        self.storage_controller.create(resource=group1, parent=None)
        self.storage_controller.create(resource=user1, parent=enterprise1)
        self.storage_controller.create(resource=user2, parent=enterprise1)
        self.storage_controller.create(resource=user3, parent=enterprise1)

        self.storage_controller.assign(resource_name=tstdk.GAUser.rest_name, resources=[user1, user2, user3], parent=group1)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=group1)
        self.assertEquals(count, 3)

        self.storage_controller.delete(user1)
        self.storage_controller.delete(user2)

        ret, count = self.storage_controller.get_all(resource_name=tstdk.GAUser.rest_name, parent=group1)
        self.assertEquals(count, 1)

