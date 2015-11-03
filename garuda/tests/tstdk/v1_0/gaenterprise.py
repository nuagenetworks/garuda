# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment



from .fetchers import GAGroupsFetcher


from .fetchers import GAUsersFetcher

from bambou import NURESTObject


class GAEnterprise(NURESTObject):
    """ Represents a Enterprise in the TST

        Notes:
            None
    """

    __rest_name__ = "enterprise"
    __resource_name__ = "enterprises"



    def __init__(self, **kwargs):
        """ Initializes a Enterprise instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> enterprise = GAEnterprise(id=u'xxxx-xxx-xxx-xxx', name=u'Enterprise')
                >>> enterprise = GAEnterprise(data=my_dict)
        """

        super(GAEnterprise, self).__init__()

        # Read/Write Attributes

        self._description = None
        self._name = None
        self._zipcode = None

        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=True)
        self.expose_attribute(local_name="zipcode", remote_name="zipcode", attribute_type=int, is_required=False, is_unique=False)


        # Fetchers


        self.groups = GAGroupsFetcher.fetcher_with_object(parent_object=self, relationship="child")


        self.users = GAUsersFetcher.fetcher_with_object(parent_object=self, relationship="child")


        self._compute_args(**kwargs)

    # Properties

    @property
    def description(self):
        """ Get description value.

            Notes:
                the desc


        """
        return self._description

    @description.setter
    def description(self, value):
        """ Set description value.

            Notes:
                the desc


        """
        self._description = value


    @property
    def name(self):
        """ Get name value.

            Notes:
                the name


        """
        return self._name

    @name.setter
    def name(self, value):
        """ Set name value.

            Notes:
                the name


        """
        self._name = value


    @property
    def zipcode(self):
        """ Get zipcode value.

            Notes:
                zip code


        """
        return self._zipcode

    @zipcode.setter
    def zipcode(self, value):
        """ Set zipcode value.

            Notes:
                zip code


        """
        self._zipcode = value



