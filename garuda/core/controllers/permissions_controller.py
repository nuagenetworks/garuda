# -*- coding: utf-8 -*-

import logging
from uuid import uuid4

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAPermissionsPlugin

logger = logging.getLogger('garuda.controller.authentication')


class GAPermissionsController(GAPluginController):
    """
    """

    DEFAULT_PERMISSION = 'read'
    PERMISSIONS = ['read', 'use', 'extend', 'write', 'all']

    def __init__(self, plugins, core_controller):
        """
        """
        super(GAPermissionsController, self).__init__(core_controller=core_controller, plugins=plugins)
        self.storage_controller = self.core_controller.storage_controller

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.permissions'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAPermissionsPlugin

    # API

    def create_permission(self, resource, target, permission, explicit=True, parent_permission_id=None):
        """
        """
        target_parent = None

        if target.parent_type and target.parent_id:
            target_parent = self.storage_controller.get(resource_name=target.parent_type, identifier=target.parent_id)

        permission_id = str(uuid4())
        key = self._compute_permission_redis_key(permission_id=permission_id,
                                                 resource_id=resource.id if hasattr(resource, 'id') else resource,
                                                 target_type=target.rest_name,
                                                 target_id=target.id,
                                                 target_parent_type=target_parent.rest_name if target_parent else 'none',
                                                 target_parent_id=target_parent.id if target_parent else 'none',
                                                 scope='E' if explicit else 'I',
                                                 parent_permission_id=parent_permission_id)

        self.redis.set(key, self._value_for_permission(permission=permission))

        if target_parent:
            self.create_permission(resource=resource,
                                   target=target_parent,
                                   permission='read',
                                   explicit=False,
                                   parent_permission_id=permission_id)

    def remove_permission(self, resource, target, permission):
        """
        """
        key_pattern = self._compute_permission_redis_key(resource_id=resource.id if hasattr(resource, 'id') else resource,
                                                         target_type=target.rest_name,
                                                         target_id=target.id)

        for key in self.redis.scan_iter(match=key_pattern):
            if self._permission_for_value(int(self.redis.get(key))) == permission:
                self._remove_implicit_child_permission(parent_permission_id=self._permission_id_from_key(key))
                self.redis.delete(key)

    def has_permission(self, resource, target, permission, explicit_only=False):
        """
        """
        key_pattern = self._compute_permission_redis_key(resource_id=resource.id if hasattr(resource, 'id') else resource,
                                                         target_type=target.rest_name,
                                                         target_id=target.id,
                                                         scope='E' if explicit_only else '*',
                                                         parent_permission_id='*')

        minimum_permission_value = self._value_for_permission(permission=permission)

        for key in self.redis.scan_iter(match=key_pattern):
            if int(self.redis.get(key)) >= minimum_permission_value:
                return True

        if not target.parent_type or not target.parent_id:
            return False

        parent_object = self.storage_controller.get(resource_name=target.parent_type, identifier=target.parent_id)

        return self.has_permission(resource=resource, target=parent_object, permission=permission, explicit_only=True)

    # Utilities

    def is_empty(self):
        """
        """
        return len(self.redis.keys('permission:*')) == 0

    def _value_for_permission(self, permission):
        """
        """
        return self.PERMISSIONS.index(permission.lower())

    def _permission_for_value(self, value):
        """
        """
        return self.PERMISSIONS[value]

    def _permission_id_from_key(self, key):
        """
        """
        return key.split(':')[1]

    def _compute_permission_redis_key(self, permission_id='*', resource_id='*', target_type='*', target_id='*',
                                      target_parent_type='*', target_parent_id='*', scope='*',
                                      parent_permission_id='*'):
        """
        """
        return 'permission:%s:%s:%s:(%s:%s;%s:%s):%s' % (permission_id, parent_permission_id,  # permissions id and hierarchy
                                                         resource_id,  # resource_id
                                                         target_type, target_id,  # target information
                                                         target_parent_type, target_parent_id,  # target parent information
                                                         scope)  # explicit/implicit

    def _remove_implicit_child_permission(self, parent_permission_id):
        """
        """
        key_pattern = self._compute_permission_redis_key(parent_permission_id=parent_permission_id)

        for key in self.redis.scan_iter(match=key_pattern):
            self._remove_implicit_child_permission(parent_permission_id=self._permission_id_from_key(key))
            self.redis.delete(key)
