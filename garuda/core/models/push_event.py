# -*- coding: utf-8 -*-

from datetime import datetime

from .abstracts import GASerializable

from garuda.core.lib.utils import VSDKLoader  # TODO: Remove this dependence !


class GAPushEvent(GASerializable):
    """

    """
    def __init__(self, action=None, entity=None):
        """
        """
        GASerializable.__init__(self)

        self.action = action
        self.entity = entity
        self.entity_type = entity.rest_resource_name if entity else None
        self.event_received_time = datetime.now()
        self.source_enterprise_id = None
        self.update_mechanism = 'DEFAULT'

        self.register_attribute(type=str, internal_name='action', name='type')
        self.register_attribute(type=object, internal_name='entity')
        self.register_attribute(type=str, internal_name='entity_type', name='entityType')
        self.register_attribute(type=datetime, internal_name='event_received_time', name='eventReceivedTime')
        self.register_attribute(type=str, internal_name='update_mechanism', name='updateMechanism')

    @classmethod
    def from_dict(cls, data):
        """
        """
        instance = super(GAPushEvent, cls).from_dict(data=data)
        instance.entity = VSDKLoader.get_instance(data['entityType'], **data['entity'])

        return instance