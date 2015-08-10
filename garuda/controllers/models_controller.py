# -*- coding: utf-8 -*-

from time import sleep


SLEEP_TIME = 0

class ModelsController(object):
    """

    """
    @classmethod
    def read(cls, *args, **kwargs):
        """
        """
        print '** Let the police...Wait for it...'
        sleep(SLEEP_TIME)
        print '...do the job **'

    @classmethod
    def get_objects(self, parent, resource_name):
        """
        """
        sleep(SLEEP_TIME)
        return [object()]

    @classmethod
    def get_object(self, resource_name, resource_value):
        """
        """
        sleep(SLEEP_TIME)
        return object()

    @classmethod
    def create_object(self, resource_name):
        """
        """
        sleep(SLEEP_TIME)
        return object()

    @classmethod
    def save_object(self, object, parent=None):
        """
        """
        sleep(SLEEP_TIME)
        return object()

    @classmethod
    def get_current_user(self):
        """
        """
        sleep(SLEEP_TIME)
        return object()
