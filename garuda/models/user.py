# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timedelta

from garuda.config import GAConfig


class GAUser(object):
    """

    """

    def __init__(self, api_key=None, id=None, avatar_data=None, avatar_type=None, creation_date=None, disabled=None, email=None, enterprise_id=None, enterprise_name=None, firstname=None, lastname=None, last_updated_by=None, last_updated_date=None, mobile_number=None, owner=None, parent_id=None, parent_type=None, password=None, role=None, username=None):
        """

        """
        self.api_key = api_key
        self.id = id
        self.avatar_data = avatar_data
        self.avatar_type = avatar_type
        self.creation_date = creation_date
        self.disabled = disabled
        self.email = email
        self.enterprise_id = enterprise_id
        self.enterprise_name = enterprise_name
        self.firstname = firstname
        self.lastname = lastname
        self.last_updated_by = last_updated_by
        self.last_updated_date = last_updated_date
        self.mobile_number = mobile_number
        self.owner = owner
        self.parent_id = parent_id
        self.parent_type = parent_type
        self.password = password
        self.role = role
        self.username = username

    def to_dict(self):
        """
        """

        to_dict = dict()

        to_dict['api_key'] = self.api_key
        to_dict['id'] = self.id
        to_dict['avatar_data'] = self.avatar_data
        to_dict['avatar_type'] = self.avatar_type
        to_dict['creation_date'] = self.creation_date
        to_dict['disabled'] = self.disabled
        to_dict['email'] = self.email
        to_dict['enterprise_id'] = self.enterprise_id
        to_dict['enterprise_name'] = self.enterprise_name
        to_dict['firstname'] = self.firstname
        to_dict['lastname'] = self.lastname
        to_dict['last_updated_by'] = self.last_updated_by
        to_dict['last_updated_date'] = self.last_updated_date
        to_dict['mobile_number'] = self.mobile_number
        to_dict['owner'] = self.owner
        to_dict['parent_id'] = self.parent_id
        to_dict['parent_type'] = self.parent_type
        to_dict['password'] = self.password
        to_dict['role'] = self.role
        to_dict['username'] = self.username

        return to_dict

    @classmethod
    def from_dict(cls, a_dict):
        ""
        ""
        instance = cls()
        instance.api_key = a_dict['api_key']
        instance.id = a_dict['id']
        instance.avatar_data = a_dict['avatar_data']
        instance.avatar_type = a_dict['avatar_type']
        instance.creation_date = a_dict['creation_date']
        instance.disabled = a_dict['disabled']
        instance.email = a_dict['email']
        instance.enterprise_id = a_dict['enterprise_id']
        instance.enterprise_name = a_dict['enterprise_name']
        instance.firstname = a_dict['firstname']
        instance.lastname = a_dict['lastname']
        instance.last_updated_by = a_dict['last_updated_by']
        instance.last_updated_date = a_dict['last_updated_date']
        instance.mobile_number = a_dict['mobile_number']
        instance.owner = a_dict['owner']
        instance.parent_id = a_dict['parent_id']
        instance.parent_type = a_dict['parent_type']
        instance.password = a_dict['password']
        instance.role = a_dict['role']
        instance.username = a_dict['username']

        return instance
