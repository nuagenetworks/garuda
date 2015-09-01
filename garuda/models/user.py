# -*- coding: utf-8 -*-

from datetime import datetime
from .abstracts import GASerializable


class GAUser(GASerializable):
    """

    """

    def __init__(self, api_key=None, id=None, avatar_data=None, avatar_type=None, creation_date=None, disabled=None, email=None, enterprise_id=None, enterprise_name=None, firstname=None, lastname=None, last_updated_by=None, last_updated_date=None, mobile_number=None, owner=None, parent_id=None, parent_type=None, password=None, role=None, username=None):
        """

        """
        GASerializable.__init__(self)

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

        self.register_attribute(type=str, internal_name='api_key')
        self.register_attribute(type=str, internal_name='id')
        self.register_attribute(type=str, internal_name='avatar_data')
        self.register_attribute(type=str, internal_name='avatar_type')
        self.register_attribute(type=datetime, internal_name='creation_date')
        self.register_attribute(type=str, internal_name='disabled')
        self.register_attribute(type=str, internal_name='email')
        self.register_attribute(type=str, internal_name='enterprise_id')
        self.register_attribute(type=str, internal_name='enterprise_name')
        self.register_attribute(type=str, internal_name='firstname')
        self.register_attribute(type=str, internal_name='lastname')
        self.register_attribute(type=str, internal_name='last_updated_by')
        self.register_attribute(type=datetime, internal_name='last_updated_date')
        self.register_attribute(type=str, internal_name='mobile_number')
        self.register_attribute(type=str, internal_name='owner')
        self.register_attribute(type=str, internal_name='parent_id')
        self.register_attribute(type=str, internal_name='parent_type')
        self.register_attribute(type=str, internal_name='password')
        self.register_attribute(type=str, internal_name='role')
        self.register_attribute(type=str, internal_name='username')
