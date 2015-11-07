from unittest import TestCase

from garuda.core.models import GAPushNotification, GAPushEvent, GARequest

from tests.tstdk import v1_0 as tstdk


class TestPushNotification(TestCase):
    """
    """
    def test_push_notification_initialization(self):
        """
        """
        entity1 = tstdk.GAEnterprise(name='enterprise1')
        event1 = GAPushEvent(action=GARequest.ACTION_CREATE, entity=entity1)
        notif = GAPushNotification(events=[event1])

        self.assertEquals(notif.events[0], event1)
        self.assertIsNotNone(notif.uuid)

    def test_push_multiple_events_order(self):
        """
        """
        entity1 = tstdk.GAEnterprise(name='enterprise1')
        entity2 = tstdk.GAEnterprise(name='enterprise2')

        event1 = GAPushEvent(action=GARequest.ACTION_UPDATE, entity=entity1)
        event2 = GAPushEvent(action=GARequest.ACTION_DELETE, entity=entity2)

        notif = GAPushNotification(events=[event1, event2])

        self.assertEquals(notif.events[0], event1)
        self.assertEquals(notif.events[1], event2)

    def test_serialize(self):
        """
        """
        self.maxDiff = None

        entity1 = tstdk.GAEnterprise(name='enterprise1')
        entity2 = tstdk.GAEnterprise(name='enterprise2')

        event1 = GAPushEvent(action=GARequest.ACTION_UPDATE, entity=entity1)
        event2 = GAPushEvent(action=GARequest.ACTION_DELETE, entity=entity2)

        notif = GAPushNotification(events=[event1, event2])
        expected = {'events': [{'entities': [{'ID': None,
                                              'creationDate': None,
                                              'description': None,
                                              'lastUpdatedDate': None,
                                              'name': 'enterprise1',
                                              'owner': None,
                                              'parentID': None,
                                              'parentType': None,
                                              'zipcode': None}],
                                'entityType': 'enterprise',
                                'type': 'UPDATE',
                                'updateMechanism': 'DEFAULT'},
                               {'entities': [{'ID': None,
                                              'creationDate': None,
                                              'description': None,
                                              'lastUpdatedDate': None,
                                              'name': 'enterprise2',
                                              'owner': None,
                                              'parentID': None,
                                              'parentType': None,
                                              'zipcode': None}],
                                'entityType': 'enterprise',
                                'type': 'DELETE',
                                'updateMechanism': 'DEFAULT'}]}

        data = notif.to_dict()

        self.assertIsNotNone(data['events'][0]['eventReceivedTime'])
        self.assertIsNotNone(data['events'][1]['eventReceivedTime'])
        self.assertIsNotNone(data['uuid'])

        del data['events'][0]['eventReceivedTime']
        del data['events'][1]['eventReceivedTime']
        del data['uuid']

        self.assertEquals(data, expected)

    def test_deserialize(self):
        """
        """
        self.maxDiff = None

        data = {'events': [{'entities': [{'ID': None,
                                          'creationDate': None,
                                          'description': None,
                                          'lastUpdatedDate': None,
                                          'name': 'enterprise1',
                                          'owner': None,
                                          'parentID': None,
                                          'parentType': None,
                                          'zipcode': None}],
                            'entityType': 'enterprise',
                            'type': 'UPDATE',
                            'updateMechanism': 'DEFAULT'},
                           {'entities': [{'ID': None,
                                          'creationDate': None,
                                          'description': None,
                                          'lastUpdatedDate': None,
                                          'name': 'enterprise2',
                                          'owner': None,
                                          'parentID': None,
                                          'parentType': None,
                                          'zipcode': None}],
                            'entityType': 'enterprise',
                            'type': 'DELETE',
                            'updateMechanism': 'DEFAULT'}],
                'uuid': 'xxx-xxx-xxx-xxx'}

        notif = GAPushNotification.from_dict(data=data)

        self.assertIsNotNone(len(notif.events), 2)
        self.assertIsNotNone(notif.uuid, 'xxx-xxx-xxx-xxx')
        self.assertIsNotNone(notif.events[0]['entities'][0]['name'], 'enterprise1')
        self.assertIsNotNone(notif.events[1]['entities'][0]['name'], 'enterprise2')
