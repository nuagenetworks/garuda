# -*- coding: utf-8 -*-

from time import sleep


class ModelsController(object):
    """

    """
    @classmethod
    def read(cls, *args, **kwargs):
        """
        """
        print '** Let the police...Wait for it...'
        sleep(2)
        print '...do the job **'

    @classmethod
    def get_objects(self, parent, resource_name):
        """
        """
        sleep(1)
        return [object()]

    @classmethod
    def get_object(self, resource_name, resource_value):
        """
        """
        sleep(1)
        return object()

    @classmethod
    def create_object(self, resource_name):
        """
        """
        sleep(1)
        return object()

    @classmethod
    def save_object(self, object, parent=None):
        """
        """
        sleep(1)
        return object()

    @classmethod
    def get_current_user(self):
        """
        """
        sleep(1)
        return object()
