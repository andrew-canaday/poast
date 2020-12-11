"""
Base type for all OpenApi 3.0 data entities.

.. seealso:: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md
"""

from abc import ABC, abstractmethod
from .exceptions import DocumentParsingException


class OpenApiEntity(ABC):
    """
    Base class for OpenAPI specification entities (objects *or* fields).
    """

    def __init__(self, data, doc_path=None):
        """
        Invoke child class initialization.
        """
        self.__doc_path = doc_path
        try:
            self._init_data(data)
        except DocumentParsingException as e:
            raise e
        except Exception as e:
            raise DocumentParsingException(
                'Error parsing element at "{}": {}'.format(
                    self.doc_path, e))
        return

    @abstractmethod
    def validate(self):
        """
        Validate the data in this object against the spec.
        """
        pass

    @property
    def openapi_type(self):
        """
        Return the name for this object, as specified by the OpenAPI 3.0 standard.

        .. seealso::
            `OAS 3.0 Schema <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#schema>`_
            for more info.

        Returns:
            str: the name for this object type, per the OAS 3.0 standard
        """
        return self.__class__.__name__

    @property
    def doc_path(self):
        """
        Return the JSON Relative Reference for this object in the document.

        .. seealso::
            `JSON Relative References <https://tools.ietf.org/html/draft-pbryan-zyp-json-ref-03>`_
            for more info.
        """
        return self.__doc_path

    def accept(self, visitor):
        """
        Traverse the object using a visitor.

        Args:
            visitor (func): a function that takes a single OpenApiEntity as an argument.

        Todo:
            - Is this really the pattern to use?
            - If so: wrap the function in an object that captures state to
              avoid cycles, etc.
        """
        return visitor(self)

    def target(self):
        """
        .. warning:: This *may* be a hack.

        This method provides access to the underlying document object in a way
        that is consistent for *both in-place and referenced objects.*
        """
        return self

    @abstractmethod
    def value(self, show_unset=False):
        """
        Subclasses MUST override to provide native python version of
        encapsulated data.
        """
        pass

    @abstractmethod
    def _init_data(self, data, doc_path):
        pass

    def __dir_unused__(self):
        """
        Make things easier on debuggers. Only show the public stuff.
        """
        for x in super().__dir__():
            if not x.startswith('_'):
                yield x
