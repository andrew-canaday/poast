"""
Base class for poast OpenApi 3.0 clients.
"""

import requests
import logging
import copy

from .basecfg import ClientConfig


class OpenApiClient:
    """
    Base class for all dynamically generated clients.

    Attributes:
        op (poast.openapi3.client.baseop.OpenApiOperations): OpenAPI operations object
        root_url (str): the root URL to which operation URI paths are appended.
        config (poast.openapi3.client.basecfg.ClientConfig): optional client configuration.
            (If absent, the default configuration is used)
        session (requests.Session): optional Session object to use for this client.
            (If absent, the session class in ``config`` is used)

    """

    __slots__ = (
        '_root_url',
        '_logger',
        '_session',
        '_request_cls',
        '_headers',
        '_cookies',
        #'auth',
    )

    def __init__(self, root_url="", config=None, session=None):
        """
        Create an instance of the API client.

        Args:
            root_url (str): the root URL to which operation URI paths are appended.
            config (poast.openapi3.client.basecfg.ClientConfig): optional client configuration.
                (If absent, the default configuration is used)
            session (requests.Session): optional Session object to use for this client.
                (If absent, the session class in ``config`` is used)

        NOTE: headers and cookies in config are copied via the `copy` module!
        """
        qualname = self.__class__.__qualname__

        # The specification dictates that path parameters MUST be appended
        # to the root url, without any resolution. Therefore, we ensure the
        # root URL has no trailing slash:
        self._root_url = root_url.rstrip("/")

        if config is None:
            config = ClientConfig()

        if config.logger is None:
            self._logger = logging.getLogger(qualname)
        else:
            self._logger = config.logger

        if session:
            self._session = session
        else:
            self._session = config.session_cls()
        self._request_cls = config.request_cls

        # Copy the headers to avoid cases where a dict shared by two or more
        # clients is modified by any one of them:
        self._headers = copy.copy(config.headers)
        self._cookies = copy.copy(config.cookies)
        return
