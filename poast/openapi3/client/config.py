"""
Base class for poast OpenAPI 3.0 client configs.
"""

import copy
import requests


class ClientConfig:
    """
    Configuration object used to customize OpenApiClient creation.

    Attributes:
        logger (logging.Logger): optional logger client created using this config
        session_cls (type): a requests.Session-like class used to create HTTP sessions
        request_cls (type): a requests.Request-like class used to create HTTP requests
        headers (dict): a list of headers common to all requests for client created from this config
        cookies (dict): a list of cookies common to all requests for client created from this config

    Notes:
     - headers and cookies are copied via the `copy` module!
    """
    __slots__ = (
        'logger',
        'session_cls',
        'request_cls',
        'headers',
        'cookies',
    )

    def __init__(self, logger=None, session_cls=None, request_cls=None,
                 headers: dict = None, cookies: dict = None):
        """
        Utility class to package up client configuration for re-use
        across multiple clients.

        NOTE: headers and cookies are copied via the `copy` module!
        """
        self.logger = logger

        if session_cls is None:
            session_cls = requests.Session
        self.session_cls = requests.Session

        if request_cls is None:
            request_cls = requests.Request
        self.request_cls = request_cls

        if headers is None:
            self.headers = {}
        else:
            self.headers = copy.copy(headers)

        if cookies is None:
            self.cookies = {}
        else:
            self.cookies = copy.copy(cookies)
        return

    def __setattr__(self, name: str, value):
        """
        Prevent anything but logger from being set to None.
        """
        if (name != 'logger') and (value is None):
            raise TypeError(
                f'{self.__class__.__qualname__}.{name} cannot be None')
        return super().__setattr__(name, value)
