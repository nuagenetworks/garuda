# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTObject

class GAAddress(NURESTObject):
    """ Represents a Group in the TST

        Notes:
            None
    """

    __rest_name__ = "address"
    __resource_name__ = "addresses"



    def __init__(self, **kwargs):
        """ Initializes a Address instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> address = GAAddress(id=u'xxxx-xxx-xxx-xxx', name=u'Address')
                >>> GAAddress = GAAddress(data=my_dict)
        """

        super(GAAddress, self).__init__()

        # Read/Write Attributes

        self._street = None

        self.expose_attribute(local_name="street", remote_name="street", attribute_type=str, is_required=False, is_unique=False)

        self._compute_args(**kwargs)

    # Properties

    @property
    def street(self):
        """ Get street value.

            Notes:
                the street


        """
        return self._street

    @street.setter
    def street(self, value):
        """ Set street value.

            Notes:
                the street


        """
        self._street = value