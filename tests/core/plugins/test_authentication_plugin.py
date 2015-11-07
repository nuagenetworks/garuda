from unittest import TestCase

from garuda.core.plugins import GAAuthenticationPlugin


class TestAuthenticationPlugin(TestCase):
    """
    """
    def test_methods(self):
        """
        """
        plugin = GAAuthenticationPlugin()
        self.assertTrue(plugin.should_manage(request='fake'))
        self.assertIsNone(plugin.extract_session_identifier(request='fake'))

    def test_auth_required(self):
        """
        """
        plugin = GAAuthenticationPlugin()

        with self.assertRaises(NotImplementedError):
            plugin.authenticate(request='request')
