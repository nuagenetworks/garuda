# -*- coding: utf-8 -*-

import logging
import redis

logger = logging.getLogger('garuda.controller.authentication')

from garuda.core.models import GAPluginController
from garuda.core.plugins import GAPermissionsPlugin


class GAPermissionsController(GAPluginController):
    """
    """

    DEFAULT_PERMISSION = 'read'
    PERMISSIONS = ['read', 'use', 'extend', 'write', 'all']

    def __init__(self, plugins, core_controller, redis_conn):
        """
        """
        super(GAPermissionsController, self).__init__(core_controller=core_controller, plugins=plugins, redis_conn=redis_conn)

    @classmethod
    def identifier(cls):
        """
        """
        return 'garuda.controller.authentication'

    @classmethod
    def managed_plugin_type(cls):
        """
        """
        return GAPermissionsPlugin

    # API

    def should_manage(self, resource, target, permission):
        """
        """
        return True

    def create_permission(self, resource, target, permission):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key=permission_key, permission=permission, implicit=False)

        if self.redis.smembers(extended_key):
            return

        self._create_permission(resource=resource, target=target, permission=permission, implicit=False)

    def remove_permission(self, resource, target, permission):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key, permission=permission, implicit=False)

        if not self.redis.smembers(self._get_extended_key(permission_key=permission_key, permission=permission, implicit=True)):
            logger.info('Remove permission %s from %s' % (permission, permission_key))
            self.redis.zrem(permission_key, permission)

        extended_implicit_keys = self.redis.smembers(extended_key)

        if extended_implicit_keys is None:
            logger.info('No implicit permissions found')
            return

        for extended_implicit_key in extended_implicit_keys:
            extended_explicit_keys = self.redis.smembers(extended_implicit_key)

            if extended_explicit_keys:
                logger.info('Found %s explicit permissions for %s' % (len(extended_explicit_keys), extended_implicit_key))

                for extended_explicit_key in extended_explicit_keys:
                    logger.info('--- %s' % extended_explicit_key)

                if len(extended_explicit_keys) == 1:
                    logger.info('Complete delete of %s' % (extended_implicit_key))
                    self.redis.delete(extended_implicit_key)

                    implicit_permission_key = self._convert_extended_key(extended_implicit_key)
                    if not self.redis.exists(self._get_extended_key(permission_key=implicit_permission_key, permission=self.DEFAULT_PERMISSION, implicit=False)):
                        logger.info('**Removes permission %s from %s' % (permission, implicit_permission_key))
                        self.redis.zrem(implicit_permission_key, self.DEFAULT_PERMISSION)

                else:
                    logger.info('Removing %s from %s' % (extended_key, extended_implicit_key))
                    self.redis.srem(extended_implicit_key, extended_key)

        self.redis.delete(extended_key)

    def has_permission(self, resource, target, permission):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)

        authorized_permission = self.redis.zrevrange(permission_key, 0, 0)

        if authorized_permission:
            permission_value = self._value_for_permission(permission=permission)
            authorized_permission_value = self._value_for_permission(permission=authorized_permission[0])

            if authorized_permission_value >= permission_value:
                logger.info('Found %s >= %s' % (authorized_permission, permission))
                return True

        if hasattr(target, "parent_object") is False:
            raise Exception('%s does not have a parent_object attribute' % target)

        parent = target.parent_object

        if parent is None:
            logger.info('No inherited permission')
            return False

        return self.has_permission(resource=resource, target=target.parent_object, permission=permission)


    # UTILITIES

    def flush_permissions(self):
        """
        """
        keys = self.redis.keys('permission*')
        self.redis.delete(*keys)

    def is_empty(self):
        """
        """
        return len(self.redis.keys('permission*')) == 0

    def _get_extended_key(self, permission_key, permission, implicit):
        """
        """
        return "%s:%s:%s" % (permission_key, permission, "I" if implicit else "E")

    def _get_permission_key(self, resource, target):
        """
        """
        return "permission:%s:%s" % (resource.id, target.id)

    def _convert_extended_key(self, extended_key):
        """
        """
        return ':'.join(extended_key.split(':')[:3])

    def _value_for_permission(self, permission):
        """
        """
        return self.PERMISSIONS.index(permission.lower())

    def _create_permission(self, resource, target, permission, implicit):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key=permission_key, permission=permission, implicit=implicit)

        permission_value = self._value_for_permission(permission=permission)
        read_value = self._value_for_permission(permission=self.DEFAULT_PERMISSION)

        logger.info('Adding permission %s (value=%s) to %s (implicit=%s)' % (permission, permission_value, permission_key, implicit))

        self.redis.zadd(permission_key, permission_value, permission)

        if hasattr(target, "parent_object") is False:
            raise Exception('%s does not have a parent_object attribute' % target)

        while target.parent_object != None:
            tmp_permission_key = self._get_permission_key(resource=resource, target=target.parent_object)
            tmp_extended_key = self._get_extended_key(permission_key=tmp_permission_key, permission=self.DEFAULT_PERMISSION, implicit=True)

            logger.info('Adding implicit %s to %s' % (tmp_extended_key, extended_key))
            logger.info('Link %s to %s' % (extended_key, tmp_extended_key))

            self.redis.sadd(extended_key, tmp_extended_key)
            self.redis.sadd(tmp_extended_key, extended_key)
            self.redis.zadd(tmp_permission_key, read_value, self.DEFAULT_PERMISSION)

            target = target.parent_object
