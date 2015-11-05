from unittest import TestCase

from garuda.core.models import GARequest


class TestRequest(TestCase):
    """
    """
    def test_response_initialization(self):
        """
        """
        request = GARequest(action=GARequest.ACTION_CREATE, channel='channel', content={'hello': 'world'}, resources='resource', username='username', token='token',
                            cookies='cookie', filter='filter', order_by='order', page=1, page_size=2, parameters={'bonjour': 'tout le monde'})

        self.assertEquals(request.action, GARequest.ACTION_CREATE)
        self.assertEquals(request.channel, 'channel')
        self.assertEquals(request.content, {'hello': 'world'})
        self.assertEquals(request.resources, 'resource')
        self.assertEquals(request.username, 'username')
        self.assertEquals(request.token, 'token')
        self.assertEquals(request.cookies, 'cookie')
        self.assertEquals(request.filter, 'filter')
        self.assertEquals(request.order_by, 'order')
        self.assertEquals(request.page, 1)
        self.assertEquals(request.page_size, 2)
        self.assertEquals(request.parameters, {'bonjour': 'tout le monde'})
        self.assertIsNotNone(request.uuid)