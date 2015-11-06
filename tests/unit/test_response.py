from unittest import TestCase

from garuda.core.models import GAResponseSuccess, GAResponseFailure


class TestResponse(TestCase):
    """
    """
    def test_response_success_initialization(self):
        """
        """
        response = GAResponseSuccess(content='hello')
        self.assertEquals(response.content, 'hello')
        self.assertIsNotNone(response.uuid)

    def test_response_failure_initialization(self):
        """
        """
        response = GAResponseFailure(content='hello')
        self.assertEquals(response.content, 'hello')
        self.assertIsNotNone(response.uuid)
