# -*- coding: utf-8 -*-

import logging
from uuid import uuid4

logger = logging.getLogger('garuda.controller')

class GAController(object):
    """
    """
    def __init__(self, core_controller, redis_conn=None):
        """
        """

        if not core_controller:
            raise Exception("core_controller must be given to all GAController subclasses")

        self._core_controller = core_controller
        self._redis           = redis_conn
        self._uuid            = str(uuid4())

    @classmethod
    def identifier(cls):
        """
        """
        raise NotImplementedError("identifier class method must be implemented")

    @property
    def core_controller(self):
        """
        """
        return self._core_controller

    @property
    def redis(self):
        """
        """
        return self._redis

    @property
    def uuid(self):
        """
        """
        return self._uuid

    def ready(self):
        """
        """
        pass

    def start(self):
        """
        """
        pass

    def stop(self):
        """
        """
        pass