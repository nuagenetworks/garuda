from unittest import TestCase

from garuda.core.models import GAPushEvent, GARequest
from garuda.core.lib import GASDKLibrary

from tests.tstdk import v1_0 as tstdk


class TestPushEvent(TestCase):
    """
    """
    def test_set_entity(self):
        """
        """
        event = GAPushEvent(action=GARequest.ACTION_CREATE)
        event.entity = 'test'

        self.assertEquals(event.entities, ['test'])
        self.assertEquals(event.entity, 'test')

    def test_set_action(self):
        """
        """
        event = GAPushEvent(action=GARequest.ACTION_CREATE)
        self.assertEquals(event.action, GARequest.ACTION_CREATE)

    def test_set_action_assign_converted_to_update(self):
        """
        """
        event = GAPushEvent()
        event.action = GARequest.ACTION_ASSIGN
        self.assertEquals(event.action, GARequest.ACTION_UPDATE)

    def test_to_dict(self):
        """
        """
        enterprise = tstdk.GAEnterprise(name='enterprise1')

        event = GAPushEvent(action=GARequest.ACTION_CREATE, entity=enterprise)

        expected_result = {'entities': [{'description': None, 'zipcode': None, 'parentType': None, 'lastUpdatedDate': None, 'parentID': None, 'owner': None, 'creationDate': None, 'ID': None, 'name': 'enterprise1'}], 'entityType': 'enterprise', 'type': 'CREATE', 'updateMechanism': 'DEFAULT'}

        converted = event.to_dict()
        del converted['eventReceivedTime']

        self.assertEqual(converted, expected_result)

    def test_from_dict(self):
        """
        """
        data = {'entities': [{'description': None, 'zipcode': None, 'parentType': None, 'lastUpdatedDate': None, 'parentID': None, 'owner': None, 'creationDate': None, 'ID': None, 'name': 'enterprise1'}], 'entityType': 'enterprise', 'type': 'CREATE', 'updateMechanism': 'DEFAULT', 'eventReceivedTime': None}
        GASDKLibrary().register_sdk('default', tstdk)
        event = GAPushEvent.from_dict(data)
        self.assertEqual(event.entity.name, 'enterprise1')
