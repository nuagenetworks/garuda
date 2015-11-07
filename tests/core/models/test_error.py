from unittest import TestCase

from garuda.core.models import GAError


class TestError(TestCase):
    """
    """
    def test_error_initialization(self):
        """
        """
        error = GAError(type=GAError.TYPE_INVALID, title='title', description='description', suggestion='nope', property_name='name')

        self.assertEquals(error.type, GAError.TYPE_INVALID)
        self.assertEquals(error.title, 'title')
        self.assertEquals(error.description, 'description')
        self.assertEquals(error.suggestion, 'nope')
        self.assertEquals(error.property_name, 'name')

    def test_serialize(self):
        """
        """
        error = GAError(type=GAError.TYPE_INVALID, title='title', description='description', suggestion='nope', property_name='name')

        expected = {'title': 'title', 'description': 'description'}
        data = error.to_dict()

        self.assertEquals(data, expected)
