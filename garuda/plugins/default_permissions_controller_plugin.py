# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('Garuda.DefaultPermissionsControllerPlugin')

import redis

from garuda.core.config import GAConfig
from garuda.core.plugins import GAPermissionsControllerPlugin


class DefaultPermissionsControllerPlugin(GAPermissionsControllerPlugin):
    """
    """
    DEFAULT_ACTION = 'read'
    ACTIONS = ['read', 'use', 'extend', 'write', 'all']

    def __init__(self, host=GAConfig.REDIS_HOST, port=GAConfig.REDIS_PORT, db=GAConfig.REDIS_DB):
        """
        """
        super(GAPermissionsControllerPlugin, self).__init__()

        self._redis = redis.StrictRedis(host=host, port=port, db=db)

    def _get_extended_key(self, permission_key, action, implicit):
        """
        """
        return "%s:%s:%s" % (permission_key, action, "I" if implicit else "E")

    def _get_permission_key(self, resource, target):
        """
        """
        return "permission:%s:%s" % (resource.id, target.id)

    def _convert_extended_key(self, extended_key):
        """
        """
        return ':'.join(extended_key.split(':')[:3])

    def _value_for_action(self, action):
        """
        """
        return DefaultPermissionsControllerPlugin.ACTIONS.index(action.lower())

    def flush_permissions(self):
        """
        """
        keys = self._redis.keys('permission*')
        self._redis.delete(*keys)

    def is_empty(self):
        """
        """
        return len(self._redis.keys('permission*')) == 0

    # Implementation

    def should_manage(self, resource, target, action):
        """
        """
        return True

    def create_permission(self, resource, target, action):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key=permission_key, action=action, implicit=False)

        if self._redis.smembers(extended_key):
            return

        self._create_permission(resource=resource, target=target, action=action, implicit=False)

    def _create_permission(self, resource, target, action, implicit):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key=permission_key, action=action, implicit=implicit)

        action_value = self._value_for_action(action=action)
        read_value = self._value_for_action(action=DefaultPermissionsControllerPlugin.DEFAULT_ACTION)

        logger.info('Adding action %s permission (value=%s) to %s (implicit=%s)' % (action, action_value, permission_key, implicit))

        self._redis.zadd(permission_key, action_value, action)

        if hasattr(target, "parent_object") is False:
            raise Exception('%s does not have a parent_object attribute' % target)

        while target.parent_object != None:
            tmp_permission_key = self._get_permission_key(resource=resource, target=target.parent_object)
            tmp_extended_key = self._get_extended_key(permission_key=tmp_permission_key, action=DefaultPermissionsControllerPlugin.DEFAULT_ACTION, implicit=True)

            logger.info('Adding implicit %s to %s' % (tmp_extended_key, extended_key))
            logger.info('Link %s to %s' % (extended_key, tmp_extended_key))

            self._redis.sadd(extended_key, tmp_extended_key)
            self._redis.sadd(tmp_extended_key, extended_key)
            self._redis.zadd(tmp_permission_key, read_value, DefaultPermissionsControllerPlugin.DEFAULT_ACTION)

            target = target.parent_object

    def remove_permission(self, resource, target, action):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)
        extended_key = self._get_extended_key(permission_key, action=action, implicit=False)

        if not self._redis.smembers(self._get_extended_key(permission_key=permission_key, action=action, implicit=True)):
            logger.info('Remove action %s permission to %s' % (action, permission_key))
            self._redis.zrem(permission_key, action)

        extended_implicit_keys = self._redis.smembers(extended_key)

        if extended_implicit_keys is None:
            logger.info('No implicit permissions found')
            return

        for extended_implicit_key in extended_implicit_keys:
            extended_explicit_keys = self._redis.smembers(extended_implicit_key)

            if extended_explicit_keys:
                logger.info('Found %s explicit permissions for %s' % (len(extended_explicit_keys), extended_implicit_key))

                for extended_explicit_key in extended_explicit_keys:
                    logger.info('--- %s' % extended_explicit_key)

                if len(extended_explicit_keys) == 1:
                    logger.info('Complete delete of %s' % (extended_implicit_key))
                    self._redis.delete(extended_implicit_key)

                    implicit_permission_key = self._convert_extended_key(extended_implicit_key)
                    if not self._redis.exists(self._get_extended_key(permission_key=implicit_permission_key, action=DefaultPermissionsControllerPlugin.DEFAULT_ACTION, implicit=False)):
                        logger.info('**Removes action %s from %s' % (action, implicit_permission_key))
                        self._redis.zrem(implicit_permission_key, DefaultPermissionsControllerPlugin.DEFAULT_ACTION)

                else:
                    logger.info('Removing %s from %s' % (extended_key, extended_implicit_key))
                    self._redis.srem(extended_implicit_key, extended_key)

        self._redis.delete(extended_key)

    def has_permission(self, resource, target, action):
        """
        """
        permission_key = self._get_permission_key(resource=resource, target=target)

        authorized_action = self._redis.zrevrange(permission_key, 0, 0)

        if authorized_action:
            action_value = self._value_for_action(action=action)
            authorized_action_value = self._value_for_action(action=authorized_action[0])

            if authorized_action_value >= action_value:
                logger.info('Found %s >= %s' % (authorized_action, action))
                return True

        if hasattr(target, "parent_object") is False:
            raise Exception('%s does not have a parent_object attribute' % target)

        parent = target.parent_object

        if parent is None:
            logger.info('No inherited permission')
            return False

        return self.has_permission(resource=resource, target=target.parent_object, action=action)
