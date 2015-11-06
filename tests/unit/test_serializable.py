from unittest import TestCase
from datetime import datetime

from garuda.core.models.abstracts import GASerializable


class SerializableObject(GASerializable):

    def __init__(self):
        """
        """
        super(SerializableObject, self).__init__()

        self.the_string = 'string'
        self.the_list = ['1', '2']
        self.the_dict = {'hello': 'world'}
        self.the_object = '3'
        self.the_float = 4.2
        self.the_int = 42
        self.the_bool = True
        self.the_none = None
        self.the_date = datetime(2015, 11, 5, 15, 27, 18, 192158)
        self.internal = 'internal'
        self.children = [SerializableObject2()]
        self.child = SerializableObject2()
        self.child_registry = {'item': SerializableObject2()}

        self.register_attribute(type=str, internal_name='the_string', name='theString')
        self.register_attribute(type=list, internal_name='the_list', name='theList')
        self.register_attribute(type=dict, internal_name='the_dict', name='theDict')
        self.register_attribute(type=object, internal_name='the_object', name='theObject')
        self.register_attribute(type=float, internal_name='the_float', name='theFloat')
        self.register_attribute(type=int, internal_name='the_int', name='theInt')
        self.register_attribute(type=datetime, internal_name='the_date', name='the_date')
        self.register_attribute(type=bool, internal_name='the_bool', name='theBool')
        self.register_attribute(type=str, internal_name='the_none', name='theNone')
        self.register_attribute(type=str, internal_name='internal')
        self.register_attribute(type=list, internal_name='children', children_type=SerializableObject2)
        self.register_attribute(type=dict, internal_name='child_registry', children_type=SerializableObject2)
        self.register_attribute(type=SerializableObject2, internal_name='child')


class SerializableObject2(GASerializable):

    def __init__(self):
        """
        """
        super(SerializableObject2, self).__init__()

        self.name = 'name'
        self.register_attribute(type=str, internal_name='name')


class TestSerializable(TestCase):
    """
    """

    def test_to_dict(self):
        """
        """
        s = SerializableObject()
        data = s.to_dict()
        self.assertEquals(data, {'internal': 'internal', 'theBool': True, 'theFloat': 4.2, 'theInt': 42, 'theObject': '3', 'the_date': '2015-11-05 15 27 18 192158',
                                 'theList': ['1', '2'], 'theDict': {'hello': 'world'}, 'theString': 'string', 'theNone': None,
                                 'children': [{'name': 'name'}], 'child': {'name': 'name'},
                                 'child_registry': {'item': {'name': 'name'}}})

    def test_from_dict(self):
        """
        """
        s = SerializableObject().from_dict({'internal': 'external', 'theBool': False, 'theFloat': 2.4, 'theInt': 24, 'theObject': '4', 'the_date': '2015-11-05 15 27 18 192158',
                                            'theList': ['3', '4'], 'theDict': {'world': 'hello'}, 'theString': 'string2', 'theNone': None,
                                            'children': [{'name': 'name'}], 'child': {'name': 'name'},
                                            'child_registry': {'item': {'name': 'name'}}})

        self.assertEquals(s.the_string, 'string2')
        self.assertEquals(s.the_list, ['3', '4'])
        self.assertEquals(s.the_dict, {'world': 'hello'})
        self.assertEquals(s.the_object, '4')
        self.assertEquals(s.the_float, 2.4)
        self.assertEquals(s.the_int, 24)
        self.assertEquals(s.the_bool, False)
        self.assertEquals(s.internal, 'external')
        self.assertEquals(s.children[0].name, 'name')
        self.assertEquals(s.child_registry['item'].name, 'name')
        self.assertEquals(s.child.name, 'name')

    def test_to_hash(self):
        """
        """
        s = SerializableObject()
        data = s.to_hash()
        self.assertEquals(data, {'internal': 'internal', 'theBool': True, 'theFloat': 4.2, 'theInt': 42, 'theObject': '3', 'the_date': '2015-11-05 15 27 18 192158',
                                 'theList': '\x92\xa11\xa12', 'theDict': '\x81\xa5hello\xa5world', 'theString': 'string', 'theNone': None,
                                 'children': ['\x81\xa4name\xa4name'], 'child': '\x81\xa4name\xa4name',
                                 'child_registry': {'item': '\x81\xa4name\xa4name'}})

    def test_from_hash(self):
        """
        """
        s = SerializableObject().from_hash({'internal': 'external', 'theBool': False, 'theFloat': 2.4, 'theInt': 24, 'theObject': '4', 'the_date': '2015-11-05 15 27 18 192158',
                                            'theList': '\x92\xa13\xa14', 'theDict': '\x81\xa5world\xa5hello', 'theString': 'string2', 'theNone': None,
                                            'children': ['\x81\xa4name\xa4name'], 'child': '\x81\xa4name\xa4name',
                                            'child_registry': {'item': '\x81\xa4name\xa4name'}})

        self.assertEquals(s.the_string, 'string2')
        self.assertEquals(s.the_list, ['3', '4'])
        self.assertEquals(s.the_dict, {'world': 'hello'})
        self.assertEquals(s.the_object, '4')
        self.assertEquals(s.the_float, 2.4)
        self.assertEquals(s.the_int, 24)
        self.assertEquals(s.the_bool, False)
        self.assertEquals(s.internal, 'external')
        self.assertEquals(s.children[0].name, 'name')
        self.assertEquals(s.child.name, 'name')
