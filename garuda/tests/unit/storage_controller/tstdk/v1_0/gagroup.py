# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment



from .fetchers import GAUsersFetcher

from bambou import NURESTObject


class GAGroup(NURESTObject):
    """ Represents a Group in the TST

        Notes:
            None
    """

    __rest_name__ = "group"
    __resource_name__ = "groups"

    

    def __init__(self, **kwargs):
        """ Initializes a Group instance

            Notes:
                You can specify all parameters while calling this methods.
                A special argument named `data` will enable you to load the
                object from a Python dictionary

            Examples:
                >>> group = GAGroup(id=u'xxxx-xxx-xxx-xxx', name=u'Group')
                >>> group = GAGroup(data=my_dict)
        """

        super(GAGroup, self).__init__()

        # Read/Write Attributes
        
        self._description = None
        self._name = None
        
        self.expose_attribute(local_name="description", remote_name="description", attribute_type=str, is_required=False, is_unique=False)
        self.expose_attribute(local_name="name", remote_name="name", attribute_type=str, is_required=True, is_unique=True)
        

        # Fetchers
        
        
        self.users = GAUsersFetcher.fetcher_with_object(parent_object=self, relationship="member")
        

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

    

    