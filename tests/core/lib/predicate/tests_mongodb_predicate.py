# -*- coding:utf-8 -*-

from unittest import TestCase
from garuda.plugins.storage import GAMongoPredicateConverter
from garuda.core.lib import GAPredicateConversionError

class TestGAMongoPredicateConverter(TestCase):
    """
    """

    def setUp(self):
        """
        """
        self.converter = GAMongoPredicateConverter()

    def assertConvertEquals(self, source, expected_result):
        """
        """
        result = self.converter.convert(source)
        self.assertEquals(result, expected_result)

    def test_strings(self):
        """
        """
        self.assertConvertEquals('name = Christophe',
                {'name': {'$eq': 'Christophe'}})

        self.assertConvertEquals('name = "Christophe"',
                {'name': {'$eq': '"Christophe"'}})

        self.assertConvertEquals('name = "Christophe" and team is "UI team"',
                {'$and': [
                    {'name': {'$eq': '"Christophe"'}},
                    {'team': {'$eq': '"UI team"'}}
                ]})

    def test_integers(self):
        """
        """
        self.assertConvertEquals('year >= 2015 and year <= 2000',
                {'$and': [
                    {'year': {'$gte': 2015}},
                    {'year': {'$lte': 2000}}
                ]})

    def test_booleans(self):
        """
        """
        self.assertConvertEquals('isValid is true and isArchived = false',
                {'$and': [
                    {'isValid': {'$eq': True}},
                    {'isArchived': {'$eq': False}}
                ]})

        self.assertConvertEquals('isValid is True and isArchived = False',
                {'$and': [
                    {'isValid': {'$eq': 'True'}},
                    {'isArchived': {'$eq': 'False'}}
                ]})

        self.assertConvertEquals('isValid = 0 and isArchived = 1',
                {'$and': [
                    {'isValid': {'$eq': 0}},
                    {'isArchived': {'$eq': 1}}
                ]})

    def test_constants(self):
        """
        """
        self.assertConvertEquals('defaultValue is null',
                    {'defaultValue': {'$eq': 'null'}})

        self.assertConvertEquals('defaultValue is empty',
                    {'defaultValue': {'$eq': ''}})

    def test_operator_or(self):
        """
        """
        self.assertConvertEquals('name = "Christophe" or name = "Antoine"',
                {'$or': [
                    {'name': {'$eq': '"Christophe"'}},
                    {'name': {'$eq': '"Antoine"'}}
                ]})

        self.assertConvertEquals('name = "Christophe" and (name = "Antoine" or name = "Alexandre")',
                {'$and': [
                    {'name': {'$eq': '"Christophe"'}},
                    { '$or': [
                        {'name': {'$eq': '"Antoine"'}},
                        {'name': {'$eq': '"Alexandre"'}}
                    ]}
                ]})

    def test_operator_not_equal(self):
        """
        """
        self.assertConvertEquals('name != "Christophe"',
                {'name': {'$ne': '"Christophe"'}})

        self.assertConvertEquals('name is not "Christophe"',
                {'name': {'$ne': '"Christophe"'}})

    def test_operator_equal(self):
        """
        """
        self.assertConvertEquals('name = "Christophe"',
                {'name': {'$eq': '"Christophe"'}})

        self.assertConvertEquals('name is "Christophe"',
                {'name': {'$eq': '"Christophe"'}})

        self.assertConvertEquals('name == "Christophe"',
                {'name': {'$eq': '"Christophe"'}})

    def test_search_id(self):
        """
        """
        self.assertConvertEquals('ID == "abcd-1234-efgh"',
                {'_id': {'$eq': '"abcd-1234-efgh"'}})

    def test_invalid_predicate(self):
        """
        """
        with self.assertRaises(GAPredicateConversionError):
            self.converter.convert('Nothing')

        with self.assertRaises(GAPredicateConversionError):
            self.converter.convert('Nothing to convert')