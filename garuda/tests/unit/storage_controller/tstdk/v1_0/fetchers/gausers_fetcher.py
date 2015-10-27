# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTFetcher


class GAUsersFetcher(NURESTFetcher):
    """ Represents a GAUsers fetcher

        Notes:
            This fetcher enables to fetch GAUser objects.

        See:
            bambou.NURESTFetcher
    """

    @classmethod
    def managed_class(cls):
        """ Return GAUser class that is managed.

            Returns:
                .GAUser: the managed class
        """

        from .. import GAUser
        return GAUser

    