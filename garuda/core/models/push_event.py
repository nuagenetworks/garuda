# -*- coding: utf-8 -*-

from datetime import datetime

from .abstracts import GASerializable


class GAPushEvent(GASerializable):
    """

    """
    def __init__(self, action=None, entities=[], entity_type=None):
        """
        """
        GASerializable.__init__(self)

        self.action = action
        self.entities = entities
        self.entity_type = entity_type
        self.event_received_time = datetime.now()
        self.source_enterprise_id = None
        self.update_mechanism = 'DEFAULT'

        self.register_attribute(type=str, internal_name='action', name='type')
        self.register_attribute(type=str, internal_name='entity_type', name='entityType')
        self.register_attribute(type=list, internal_name='entities')
        self.register_attribute(type=datetime, internal_name='event_received_time', name='eventReceivedTime')
        self.register_attribute(type=str, internal_name='update_mechanism', name='updateMechanism')
