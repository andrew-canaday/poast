"""
Base class for poast OpenAPI 3.0 endpoint operations.
"""

from weakref import proxy


class OpenApiOperations:
    """
    Base class for all dynamically generated operations.
    """

    __slots__ = (
        '__weakref__',
        '_client',
    )

    def __init__(self, client):
        """
        Create an instance of the operation.
        """
        self._client = proxy(client)
        return
