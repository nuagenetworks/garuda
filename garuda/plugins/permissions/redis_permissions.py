# -*- coding: utf-8 -*-

import logging
from uuid import uuid4

from garuda.core.models import GAPluginManifest
from garuda.core.plugins import GAPermissionsPlugin

logger = logging.getLogger('garuda.controller.permission.redis')


class GARedisPermissionsPlugin(GAPermissionsPlugin):
    """
    """

    SYSTEM_PERMISSION = 'garuda-system-permission'
    DEFAULT_PERMISSION = 'read'
    PERMISSIONS = ['read', 'use', 'extend', 'write', 'all']

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.permissions.redis'

    @classmethod
    def manifest(cls):
        """
        """
        return GAPluginManifest(name='redis_permissions', version=1.0, identifier='garuda.controller.permissions.redis')

    def should_manage(self):
        """
        """
        return True

    # Properties

    @property
    def storage_controller(self):
        """
        """
        return self.core_controller.storage_controller

    @property
    def redis(self):
        """
        """
        return self.core_controller.redis

    # API

    def create_permission(self, resource, target, permission, explicit=True, parent_permission_id=None):
        """
        """
        target_parent = None

        if target.parent_type and target.parent_id:
            response = self.storage_controller.get(user_identifier=self.SYSTEM_PERMISSION, resource_name=target.parent_type, identifier=target.parent_id)
            target_parent = response.data

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
                self._remove_implicit_child_permission(parent_permission_id=self._extract_permission_id_from_key(key))
                self.redis.delete(key)

    def remove_all_permissions_of_resource(self, resource):
        """
        """
        key_pattern = self._compute_permission_redis_key(resource_id=resource.id if hasattr(resource, 'id') else resource)
        keys = list(self.redis.scan_iter(match=key_pattern))
        self.redis.delete(*keys)

    def remove_all_permissions_for_target_ids(self, target_ids):
        """
        """
        keys = []

        for key in self.redis.scan_iter(match='permission:*'):
            if key.split(":")[5] in target_ids:
                keys.append(key)

        if len(keys):
            self.redis.delete(*keys)

    def has_permission(self, resource, target, permission, explicit_only=False):
        """
        """
        if resource == self.SYSTEM_PERMISSION:
            return True

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

        response = self.storage_controller.get(user_identifier=self.SYSTEM_PERMISSION, resource_name=target.parent_type, identifier=target.parent_id)
        target_parent = response.data

        return self.has_permission(resource=resource, target=target_parent, permission=permission, explicit_only=True)

    def child_ids_with_permission(self, resource, parent_id, children_type, permission=None):
        """
        """
        key_pattern = self._compute_permission_redis_key(resource_id=resource.id if hasattr(resource, 'id') else resource,
                                                         target_type=children_type if children_type else '*',
                                                         target_parent_id=parent_id if parent_id else '*')

        permission_value = self._value_for_permission(permission) if permission else 0

        ids = set()
        for key in self.redis.scan_iter(match=key_pattern):

            if permission_value == 0:  # in that case, no need to query redis for the value, any permission will do
                ids.add(self._extract_target_from_key(key))
                continue

            if int(self.redis.get(key)) >= permission_value:
                ids.add(self._extract_target_from_key(key))

        return ids

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

    def _extract_permission_id_from_key(self, key):
        """
        """
        return key.split(':')[1]

    def _extract_target_from_key(self, key):
        """
        """
        return key.split(':')[5]

    def _compute_permission_redis_key(self, permission_id='*', parent_permission_id='*', resource_id='*', target_type='*',
                                      target_id='*', target_parent_type='*', target_parent_id='*', scope='*'):
        """
        """
        # permission:pid:ppid:rid:ttype:tid:tptype:tpid:s

        return 'permission:%s:%s:%s:%s:%s:%s:%s:%s' % (permission_id, parent_permission_id,  # permissions id and hierarchy
                                                       resource_id,  # resource_id
                                                       target_type, target_id,  # target information
                                                       target_parent_type, target_parent_id,  # target parent information
                                                       scope)  # explicit/implicit

    def _remove_implicit_child_permission(self, parent_permission_id):
        """
        """
        key_pattern = self._compute_permission_redis_key(parent_permission_id=parent_permission_id)

        pipeline = self.redis.pipeline()
        pipeline.multi()
        for key in self.redis.scan_iter(match=key_pattern):
            self._remove_implicit_child_permission(parent_permission_id=self._extract_permission_id_from_key(key))
            pipeline.delete(key)
        pipeline.execute()
