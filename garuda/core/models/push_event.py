# -*- coding: utf-8 -*-

from datetime import datetime

from .abstracts import GASerializable
from garuda.core.lib import SDKLibrary

class GAPushEvent(GASerializable):
    """

    """

    UPDATE_MECHANISM_DEFAULT = 'DEFAULT'
    UPDATE_MECHANISM_REFETCH = 'REFETCH'
    UPDATE_MECHANISM_REFETCH_HIERARCHY = 'REFETCH_HIERARCHY'

    def __init__(self, action=None, entity=None):
        """
        """
        super(GAPushEvent, self).__init__()

        self.action = action
        self.entities = [entity]
        self.entity_type = entity.rest_name if entity else None
        self.event_received_time = datetime.now()
        self.source_enterprise_id = None
        self.update_mechanism = self.UPDATE_MECHANISM_DEFAULT

        self.register_attribute(type=str, internal_name='action', name='type')
        self.register_attribute(type=list, internal_name='entities')
        self.register_attribute(type=str, internal_name='entity_type', name='entityType')
        self.register_attribute(type=datetime, internal_name='event_received_time', name='eventReceivedTime')
        self.register_attribute(type=str, internal_name='update_mechanism', name='updateMechanism')

    @property
    def entity(self):
        return self.entities[0] if self.entities and len(self.entities) else None

    @entity.setter
    def entity(self, value):
        self.entities = [value]

    @classmethod
    def from_dict(cls, data):
        """
        """
        instance = super(GAPushEvent, cls).from_dict(data=data)
        instance.entities = [SDKLibrary().get_instance(data['entityType'], **data['entities'][0])]

        return instance
