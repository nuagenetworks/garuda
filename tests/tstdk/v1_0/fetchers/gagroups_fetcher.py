# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTFetcher


class GAGroupsFetcher(NURESTFetcher):
    """ Represents a GAGroups fetcher

        Notes:
            This fetcher enables to fetch GAGroup objects.

        See:
            bambou.NURESTFetcher
    """

    @classmethod
    def managed_class(cls):
        """ Return GAGroup class that is managed.

            Returns:
                .GAGroup: the managed class
        """

        from .. import GAGroup
        return GAGroup

