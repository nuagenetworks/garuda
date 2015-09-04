# -*- coding: utf-8 -*-

import logging
import json

from collections import namedtuple
from datetime import datetime

from garuda.core.config import GAConfig

GASerializableAttribute = namedtuple('GASerializableAttribute', ['internal_name', 'name', 'type', 'children_type'])


logger = logging.getLogger('Garuda.Serializable')

class GASerializable(object):
    """

    """
    def __init__(self):
        """
        """
        self._attributes = []

    def register_attribute(self, type, internal_name, name=None, children_type=None):
        """
        """
        if name is None:
            name = internal_name[1:] if internal_name.startswith('_') else internal_name

        attribute = GASerializableAttribute(internal_name=internal_name, name=name, type=type, children_type=children_type)
        self._attributes.append(attribute)

    # Hashing for Redis

    def to_hash(self):
        """
        """
        return self.to_dict(hash_children=True)

    @classmethod
    def from_hash(cls, adict):
        """
        """
        return cls.from_dict(data=adict, hash_children=True)

    # Basic Serialization

    def to_dict(self, hash_children=False):
        """
        """
        result = dict()

        for attribute in self._attributes:
            value = getattr(self, attribute.internal_name)

            if attribute.type is dict and len(value) > 0:
                result[attribute.name] = dict()
                # try:
                keys = value.keys()
                # except:
                #     print self
                #     print self.user_info
                #     print type(self.user_info)
                #     raise Exception('stop')
                key = keys[0]

                object = value[key]

                if hasattr(object, 'to_dict'):

                    for key in keys:

                        d = value[key].to_dict()
                        result[attribute.name][key] = json.dumps(d) if hash_children else d

                else:
                    result[attribute.name] = json.dumps(value) if hash_children else value

            elif attribute.type is list and len(value) > 0:
                result[attribute.name] = list()
                object = value[0]

                if hasattr(object, 'to_dict'):
                    for object in value:
                        d = object.to_dict()
                        result[attribute.name].append(json.dumps(d) if hash_children else d)

                else:
                    result[attribute.name] = json.dumps(value) if hash_children else value

            elif value is not None and hasattr(value, 'to_dict'):
                d = value.to_dict()
                result[attribute.name] = json.dumps(d) if hash_children else d

            elif value is not None and attribute.type is datetime:
                result[attribute.name] = value.strftime(GAConfig.DATE_FORMAT)

            else:
                result[attribute.name] = value

        return result

    @classmethod
    def from_dict(cls, data, hash_children=False):
        """
        """
        instance = cls()

        for attribute in instance._attributes:

            value = data[attribute.name]

            # Dictionary
            if attribute.type is dict:
                if attribute.children_type and hasattr(attribute.children_type, 'to_dict'):
                    attribute_value = attribute.type()
                    for key in value.keys():
                        object = value[key]
                        d = json.loads(object) if hash_children else object
                        attribute_value[key] = attribute.children_type.from_dict(d)

                    setattr(instance, attribute.internal_name, attribute_value)
                else:
                    setattr(instance, attribute.internal_name, json.loads(value) if hash_children else value)
            # List
            elif attribute.type is list:
                if attribute.children_type and hasattr(attribute.children_type, 'to_dict'):
                    attribute_value = attribute.type()
                    for object in value:
                        d = json.loads(object) if hash_children else object
                        attribute_value.append(attribute.children_type.from_dict(d))

                    setattr(instance, attribute.internal_name, attribute_value)
                else:
                    setattr(instance, attribute.internal_name, json.loads(value) if hash_children else value)

            elif value is not None:

                # Objects
                if hasattr(attribute.type, 'to_dict'):
                    object = attribute.type()  # Note: Allows to use NURESTObject as well
                    d = json.loads(value) if hash_children else value
                    value = object.from_dict(d)
                    setattr(instance, attribute.internal_name, value if value else object)

                # Datetime
                elif attribute.type is datetime:
                    setattr(instance, attribute.internal_name, datetime.strptime(value, GAConfig.DATE_FORMAT))

                # Boolean
                elif attribute.type is bool:
                    setattr(instance, attribute.internal_name, True if value == "True" else False)

                # Others
                else:
                    setattr(instance, attribute.internal_name, value)
            # None
            else:
                setattr(instance, attribute.internal_name, None)

        return instance
