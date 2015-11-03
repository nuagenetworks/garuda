# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTSession
from bambou.exceptions import InternalConsitencyError
from .garoot import GARoot


class GATSTSession(NURESTSession):
    """ TST User Session

        Session can be started and stopped whenever its needed
    """

    def __init__(self, username, enterprise, api_url, password=None, certificate=None):
        """ Initializes a new sesssion

            Args:
                username (string): the username
                password (string): the password
                enterprise (string): the enterprise
                api_url (string): the url to the api

            Example:
                >>> session =  GAtstSession(username="csproot", password="csproot", enterprise="csp", api_url="https://TST:8443")
                >>> session.start()

        """

        if certificate is None and password is None:
            raise InternalConsitencyError('GAtstSession needs either a password or a certificate')

        super(GATSTSession, self).__init__(username=username, password=password, enterprise=enterprise, api_url=api_url, api_prefix="api", version=str(self.version), certificate=certificate)

    @property
    def version(self):
        """ Returns the current TST version

        """
        return 1.0

    @property
    def root(self):
        """ Returns the root object

        """
        return self.root_object

    @classmethod
    def create_root_object(self):
        """ Returns a new instance

        """
        return GARoot()

    