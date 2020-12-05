"""
Poast OpTable.
"""

from weakref import proxy


class OpTable:
    """
    API Operations Table.
    """

    __slots__ = (
        '__weakref__',
        '_client',
    )

    def __init__(self, client, operations=None):
        """
        Create an instance of the operation.
        """
        if operations is None:
            operations = tuple()

        # for op in operations:
        #     self._add_operation(op)

        self._client = proxy(client)
        return
