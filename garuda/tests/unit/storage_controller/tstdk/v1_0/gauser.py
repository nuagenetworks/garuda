# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment


from bambou import NURESTObject
from .fetchers import GAAddressesFetcher

class GAUser(NURESTObject):
    """ Represents a User in the TST

        Notes:
            None
    """

    __rest_name__ = "user"
    __resource_name__ = "users"



    def __init__(self, **kwargs):
        """ Initializes a User instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> user = GAUser(id=u'xxxx-xxx-xxx-xxx', name=u'User')
                >>> user = GAUser(data=my_dict)
        """

        super(GAUser, self).__init__()

        # Read/Write Attributes

        self._full_name = None
        self._username = None

        self.expose_attribute(local_name="full_name", remote_name="fullName", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="username", remote_name="username", attribute_type=str, is_required=True, is_unique=True)

        self.addresses = GAAddressesFetcher.fetcher_with_object(parent_object=self, relationship="child")

        self._compute_args(**kwargs)

    # Properties

    @property
    def full_name(self):
        """ Get full_name value.

            Notes:
                the full name


                This attribute is named `fullName` in TST API.

        """
        return self._full_name

    @full_name.setter
    def full_name(self, value):
        """ Set full_name value.

            Notes:
                the full name


                This attribute is named `fullName` in TST API.

        """
        self._full_name = value


    @property
    def username(self):
        """ Get username value.

            Notes:
                the username


        """
        return self._username

    @username.setter
    def username(self, value):
        """ Set username value.

            Notes:
                the username


        """
        self._username = value



