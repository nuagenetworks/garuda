# -*- coding: utf-8 -*-

from datetime import datetime

from .abstracts import GASerializable
from garuda.core.lib import SDKsManager

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
        self.entity = entity
        self.entity_type = entity.rest_resource_name if entity else None
        self.event_received_time = datetime.now()
        self.source_enterprise_id = None
        self.update_mechanism = self.UPDATE_MECHANISM_DEFAULT

        self.register_attribute(type=str, internal_name='action', name='type')
        self.register_attribute(type=object, internal_name='entity')
        self.register_attribute(type=str, internal_name='entity_type', name='entityType')
        self.register_attribute(type=datetime, internal_name='event_received_time', name='eventReceivedTime')
        self.register_attribute(type=str, internal_name='update_mechanism', name='updateMechanism')

    @classmethod
    def from_dict(cls, data):
        """
        """
        sdk_manager = SDKsManager()

        instance = super(GAPushEvent, cls).from_dict(data=data)
        instance.entity = sdk_manager.get_instance(data['entityType'], **data['entity'])

        return instance
