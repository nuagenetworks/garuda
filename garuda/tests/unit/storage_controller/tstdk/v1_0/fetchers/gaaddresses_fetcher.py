# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTFetcher


class GAAddressesFetcher(NURESTFetcher):
    """ Represents a GAAddresse fetcher

        Notes:
            This fetcher enables to fetch GAAddress objects.

        See:
            bambou.NURESTFetcher
    """

    @classmethod
    def managed_class(cls):
        """ Return GAAddress class that is managed.

            Returns:
                .GAAddress: the managed class
        """

        from .. import GAAddress
        return GAAddress