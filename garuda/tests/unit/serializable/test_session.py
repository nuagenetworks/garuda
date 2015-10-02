# -*- coding: utf-8 -*-

import json
from datetime import datetime

from vspk.vsdk.v3_2 import NURESTUser

from garuda.tests import UnitTestCase
from garuda.core.models import GASession


def get_valid_user():
    """
    """
    user = NURESTUser()
    user.id = '5555-5555-5555'
    user.first_name = 'Christophe'
    user.last_name = 'Serafin'
    user.user_name = 'serafinc'
    user.api_key = 'ABC-DEF-GHI'
    user.is_valid = True
    # user.creation_date = datetime.now()

    return user


class TestSerializeSession(UnitTestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        """ Initialize context

        """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Removes context

        """
        pass

    def test_session_to_dict(self):
        """ Session should be serializable as a dictionary

        """
        user = get_valid_user()

        session = GASession(garuda_uuid='xxx-yyy-zzzz', user=user, user_info={'APIKey': '12345678'})

        expected_result = {
            'is_listening_push_notifications': False,
            'user_info': {'APIKey': '12345678'},
            'garuda_uuid': 'xxx-yyy-zzzz',
            'uuid': session.uuid,
            'user': user.to_dict()
        }

        self.assertEqual(session.to_dict(), expected_result)

    def test_session_to_hash(self):
        """ Session should be serializable as a hashmap

        """
        user = get_valid_user()

        session = GASession(garuda_uuid='xxx-yyy-zzzz', user=user, user_info={'APIKey': '12345678'})

        expected_result = {
            'is_listening_push_notifications': False,
            'user_info': '{"APIKey": "12345678"}',
            'garuda_uuid': 'xxx-yyy-zzzz',
            'uuid': session.uuid,
            'user': json.dumps(user.to_dict())
        }

        self.assertEqual(session.to_hash(), expected_result)


class TestDeserializeSession(UnitTestCase):
    """
    """
    @classmethod
    def setUpClass(cls):
        """ Initialize context """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Removes context """
        pass

    def test_session_from_dict(self):
        """ Session should be deserializable from a dictionary

        """
        user = get_valid_user()

        session = GASession(garuda_uuid='xxx-yyy-zzzz', user=user, user_info={'APIKey': '12345678'})
        d = session.to_dict()

        deserialized_session = GASession.from_dict(d)

        self.assertNotEqual(deserialized_session.user, None)
        self.assertEqual(deserialized_session.to_dict(), d)

    def test_session_from_hash(self):
        """ Session should be deserializable from a hashmap

        """
        user = get_valid_user()

        session = GASession(garuda_uuid='xxx-yyy-zzzz', user=user, user_info={'APIKey': '12345678'})
        h = session.to_hash()

        deserialized_session = GASession.from_hash(h)

        self.assertEqual(deserialized_session.to_hash(), h)