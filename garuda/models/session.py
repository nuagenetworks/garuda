# -*- coding: utf-8 -*-

import json

from uuid import uuid4

from .user import GAUser


class GASession(object):
    """

    """

    HOUR_TO_LIVE = 3600

    def __init__(self, garuda_uuid=None, user=None, user_info={}):
        """

        """
        self.hash_attributes = ['_uuid', '_garuda_uuid', 'user', 'user_info', 'is_listening_push_notifications']

        self._uuid = str(uuid4())
        self._garuda_uuid = garuda_uuid
        self.user = user
        self.user_info = user_info
        self.is_listening_push_notifications = False

    @property
    def uuid(self):
        """
        """
        return self._uuid

    @property
    def garuda_uuid(self):
        """
        """
        return self._garuda_uuid

    # Conversion / Serialization

    def to_hash(self):
        """
        """
        result = dict()

        for attribute_name in self.hash_attributes:
            hash_name = attribute_name[1:] if attribute_name.startswith('_') else attribute_name
            attribute = getattr(self, attribute_name)
            attribute_type = type(attribute)

            if attribute_type is dict or attribute_type is list:
                result[hash_name] = json.dumps(attribute)

            elif attribute_type is object:
                result[hash_name] = json.dumps(attribute.to_dict())

            else:
                result[hash_name] = attribute

        return result

    @classmethod
    def from_hash(cls, adict):
        """
        """
        instance = cls()

        for attribute_name in instance.hash_attributes:
            hash_name = attribute_name[1:] if attribute_name.startswith('_') else attribute_name
            attribute = getattr(instance, attribute_name)
            attribute_type = type(attribute)

            value = adict[hash_name]

            if attribute_type is dict or attribute_type is list:
                setattr(instance, attribute_name, json.loads(value))

            elif attribute_type is object:
                setattr(instance, attribute_name, json.loads(attribute_type.from_dict()))

            else:
                setattr(instance, attribute_name, value)

        return instance

    def to_dict(self):
        """
        """

        to_dict = dict()

        to_dict['uuid'] = self._uuid
        to_dict['garuda_uuid'] = self.garuda_uuid
        to_dict['user'] = self.user.to_dict()
        to_dict['user_info'] = self.user_info
        to_dict['is_listening_push_notifications'] = self.is_listening_push_notifications

        return to_dict

    @classmethod
    def from_dict(cls, a_dict):
        """
        """
        instance = cls()

        instance._uuid = a_dict['uuid']
        instance._garuda_uuid = a_dict['garuda_uuid']
        instance.user = GAUser.from_dict(a_dict['user'])
        instance.user_info = a_dict['user_info']
        instance.is_listening_push_notifications = a_dict['is_listening_push_notifications']

        return instance
