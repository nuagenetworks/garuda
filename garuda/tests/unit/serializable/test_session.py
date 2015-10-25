# -*- coding: utf-8 -*-

import json
from datetime import datetime

from garuda.tests import UnitTestCase
from garuda.core.models import GASession


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
        session = GASession(garuda_uuid='xxx-yyy-zzzz')

        expected_result = {
            'garuda_uuid': 'xxx-yyy-zzzz',
            'root_object': None,
            'uuid': session.uuid
        }

        self.assertEqual(session.to_dict(), expected_result)

    def test_session_to_hash(self):
        """ Session should be serializable as a hashmap

        """
        session = GASession(garuda_uuid='xxx-yyy-zzzz')

        expected_result = {
            'garuda_uuid': 'xxx-yyy-zzzz',
            'root_object': None,
            'uuid': session.uuid,
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
        session = GASession(garuda_uuid='xxx-yyy-zzzz')
        d = session.to_dict()

        deserialized_session = GASession.from_dict(d)

        self.assertEqual(deserialized_session.to_dict(), d)

    def test_session_from_hash(self):
        """ Session should be deserializable from a hashmap

        """
        session = GASession(garuda_uuid='xxx-yyy-zzzz')
        h = session.to_hash()

        deserialized_session = GASession.from_hash(h)

        self.assertEqual(deserialized_session.to_hash(), h)