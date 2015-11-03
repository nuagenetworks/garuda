# -*- coding: utf-8 -*-
#
# No Header
#
# to add a custom header, add a file
# named __code_header in your sdk user vanilla
# and add whatever header you like
# Don't forget to make it a comment

from bambou import NURESTFetcher


class GAEnterprisesFetcher(NURESTFetcher):
    """ Represents a GAEnterprises fetcher

        Notes:
            This fetcher enables to fetch GAEnterprise objects.

        See:
            bambou.NURESTFetcher
    """

    @classmethod
    def managed_class(cls):
        """ Return GAEnterprise class that is managed.

            Returns:
                .GAEnterprise: the managed class
        """

        from .. import GAEnterprise
        return GAEnterprise

    