# -*- coding: utf-8 -*-

from .models_controller import ModelsController

class AuthenticationController(object):
    """

    """
    def authenticate(self, request, models_controller):
        """
        """

        if 'username' not in request.parameters or \
           'password' not in request.parameters or \
           'X-Nuage-Organization' not in request.parameters:
           return None

        username = request.parameters['username']
        password = request.parameters['password']
        enterprise = request.parameters['X-Nuage-Organization']

        return models_controller.authenticate_user(username=username, password=password, enterprise=enterprise)

