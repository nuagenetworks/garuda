# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment



from .fetchers import GAEnterprisesFetcher

from bambou import NURESTRootObject


class GARoot(NURESTRootObject):
    """ Represents a Root in the TST

        Notes:
            None
    """

    __rest_name__ = "root"
    __resource_name__ = "root"



    def __init__(self, **kwargs):
        """ Initializes a Root instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> root = GARoot(id=u'xxxx-xxx-xxx-xxx', name=u'Root')
                >>> root = GARoot(data=my_dict)
        """

        super(GARoot, self).__init__()

        # Read/Write Attributes




        # Fetchers


        self.enterprises = GAEnterprisesFetcher.fetcher_with_object(parent_object=self, relationship="child")


        self._compute_args(**kwargs)

    # Properties


