"""
Base request wrapper class for poast OpenApi 3.0 clients.
"""
from weakref import proxy

class RequestExecutor:
    """
    Class that wraps a :class:`requests.Request` and :class:`requests.Session`
    object to facilitate optional modification of request before executing.

    Attributes:
        request (requests.PreparedRequest): the prepared request just prior to transmission
    """

    __slots__ = (
        '__weakref__',
        '_session',
        'request',
    )

    def __init__(self, session, request):
        """
        Initialize a wrapper request with a given session and prepared request.

        Args:
            session (requests.Session): the session object used to execute the operation
            request (requests.Request): the request object used to execute the operation
        """
        # Use a weakref for the session so that clients don't live just
        # because request objects have a non-zero reference count:
        self._session = proxy(session)
        self._request = request

    def __call__(self, **kwargs):
        """
        Send the prepared request using the client's session.

        Args:
            **kwargs: Keyword arguments passed to :func:`requests.Session.send`
        """
        return self._session.send(self._request, **kwargs)

