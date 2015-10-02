# -*- coding: utf-8 -*-

from garuda.tests.unit.permissions import PermissionPluginTestCase


class TestCreatePermissions(PermissionPluginTestCase):
    """
    """

    def setUp(self):
        """ Initialize context

        """
        pass

    def tearDown(self):
        """ Cleanup context

        """
        pass

    def test_create_read_permission_at_root_level(self):
        """ Permission READ at the top level should be inherited

        """
        self.grant_permission(self.objectA, 'read')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanNotUse(self.objectC)
        self.assertCanNotUse(self.objectD)
        self.assertCanNotUse(self.objectE)
        self.assertCanNotUse(self.objectF)
        self.assertCanNotUse(self.objectG)

        self.revoke_permission(self.objectA, 'read')

    def test_create_read_permission_at_object_level(self):
        """ Permission READ at the top level should be inherited and implicitely extended

        """
        self.grant_permission(self.objectC, 'read')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanNotUse(self.objectC)
        self.assertCanNotUse(self.objectD)
        self.assertCanNotUse(self.objectE)
        self.assertCanNotUse(self.objectF)
        self.assertCanNotUse(self.objectG)

        self.revoke_permission(self.objectC, 'read')


    def test_create_use_permission_at_root_level(self):
        """ Permission USE at the top level should be inherited and implicitely extended

        """

        self.grant_permission(self.objectC, 'use')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanNotWrite(self.objectB)
        self.assertCanNotWrite(self.objectC)
        self.assertCanNotWrite(self.objectD)
        self.assertCanNotWrite(self.objectE)
        self.assertCanNotWrite(self.objectF)
        self.assertCanNotWrite(self.objectG)

        self.revoke_permission(self.objectC, 'use')


class TestOverridePermissions(PermissionPluginTestCase):
    """
    """
    def setUp(self):
        """ Initialize context

        """
        self.grant_permission(self.objectC, 'use')

    def tearDown(self):
        """ Cleanup context

        """
        self.revoke_permission(self.objectC, 'use')

    def test_override_write_permission_before_object(self):
        """ Permission WRITE before an existing USE permission should override it
        """
        self.grant_permission(self.objectB, 'write')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanWrite(self.objectB)
        self.assertCanWrite(self.objectC)
        self.assertCanWrite(self.objectD)
        self.assertCanWrite(self.objectE)
        self.assertCanWrite(self.objectF)
        self.assertCanWrite(self.objectG)

        self.revoke_permission(self.objectB, 'write')


    def test_override_write_permission_after_object(self):
        """ Permission WRITE after an existing USE permission should override it
        """
        self.grant_permission(self.objectF, 'write')

        # Read
        self.assertCanRead(self.objectA)
        self.assertCanRead(self.objectB)
        self.assertCanRead(self.objectC)
        self.assertCanRead(self.objectD)
        self.assertCanRead(self.objectE)
        self.assertCanRead(self.objectF)
        self.assertCanRead(self.objectG)

        # Use
        self.assertCanNotUse(self.objectA)
        self.assertCanNotUse(self.objectB)
        self.assertCanUse(self.objectC)
        self.assertCanUse(self.objectD)
        self.assertCanUse(self.objectE)
        self.assertCanUse(self.objectF)
        self.assertCanUse(self.objectG)

        # Write
        self.assertCanNotWrite(self.objectA)
        self.assertCanNotWrite(self.objectB)
        self.assertCanNotWrite(self.objectC)
        self.assertCanNotWrite(self.objectD)
        self.assertCanNotWrite(self.objectE)
        self.assertCanWrite(self.objectF)
        self.assertCanWrite(self.objectG)

        self.revoke_permission(self.objectF, 'write')
