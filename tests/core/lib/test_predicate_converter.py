from unittest import TestCase

from garuda.core.lib import GAPredicateConverter


class TestPredicateConverter(TestCase):
    """
    """

    def test_convert_tree(self):
        """
        """
        c = GAPredicateConverter()

        with self.assertRaises(NotImplementedError):
            c.convert_tree(ast=None)

    def test_convert_with_bad_predicate(self):
        """
        """
        c = GAPredicateConverter()

        with self.assertRaises(SyntaxError):
            c.convert(source='nope')

        with self.assertRaises(SyntaxError):
            c.convert(source='nope == "')

        with self.assertRaises(SyntaxError):
            c.convert(source='hello world wesh ta vu')

        with self.assertRaises(SyntaxError):
            c.convert(source='nope == test"')
