from unittest import TestCase

from garuda.channels.rest.parser import GAPathParser


class TestPathParser(TestCase):
    """
    """

    def test_parse_root_resource(self):
        """
        """
        parser = GAPathParser()
        result = parser.parse(path='/v1_0/root', url_prefix='api')

        self.assertEquals(len(result), 1)
        self.assertEquals(parser.version, 'v1_0')
        self.assertEquals(result[0].name, 'root')
        self.assertEquals(result[0].value, None)

    def test_parse_self_resource(self):
        """
        """
        parser = GAPathParser()
        parser.parse(path='/v1_0/enterprises/xxx', url_prefix='api')

        self.assertEquals(len(parser.resources), 1)
        self.assertEquals(parser.resources[0].name, 'enterprise')
        self.assertEquals(parser.resources[0].value, 'xxx')

    def test_parse_child_resource(self):
        """
        """
        parser = GAPathParser()
        parser.parse(path='/v1_0/enterprises/xxx/users', url_prefix='api')

        self.assertEquals(len(parser.resources), 2)
        self.assertEquals(parser.resources[0].name, 'enterprise')
        self.assertEquals(parser.resources[0].value, 'xxx')

        self.assertEquals(parser.resources[1].name, 'user')
        self.assertEquals(parser.resources[1].value, None)

    def test_root(self):
        """
        """
        parser = GAPathParser()
        parser.parse(path='', url_prefix='api')

        self.assertEquals(len(parser.resources), 0)

    def test_parse_events(self):
        """
        """
        parser = GAPathParser()
        parser.parse(path='/v1_0/events', url_prefix='api')

        self.assertEquals(len(parser.resources), 1)
        self.assertEquals(parser.resources[0].name, 'event')
        self.assertEquals(parser.resources[0].value, None)

    def test_resource_mappings(self):
        """
        """
        parser = GAPathParser(resource_mappings={'totos': 'enterprises'})
        parser.parse(path='/v1_0/totos', url_prefix='api')

        self.assertEquals(len(parser.resources), 1)
        self.assertEquals(parser.resources[0].name, 'enterprise')
        self.assertEquals(parser.resources[0].value, None)
