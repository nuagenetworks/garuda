# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('Garuda.AuthenticationController')

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
           logger.debug("No information provided to authenticate user")
           return None

        username = request.parameters['username']
        password = request.parameters['password']
        enterprise = request.parameters['X-Nuage-Organization']


        logger.debug("Authenticate user with username=%s, password=%s, enterprise=%s" % (username, password, enterprise))
        return models_controller.authenticate_user(username=username, password=password, enterprise=enterprise)

