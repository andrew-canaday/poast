"""
OpenApi 3.0 Reference type.

For more information, see:
 - https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#referenceObject
"""

from .entity import OpenApiEntity
from .exceptions import MalformedDocumentException


# TODO: This should subclass OpenApiBaseObject...
class ReferenceObject(OpenApiEntity):
    def _init_data(self, data):
        self.__data = data
        self.__ref = data.get("$ref")
        self.__obj = None

    def __getattr__(self, name):
        if self.__obj:
            return getattr(self.__obj, name)
        else:
            raise ValueError('Unresolved reference: "{}" at "{}"'.format(
                self.__ref, self.doc_path))

    @property
    def ref(self):
        return self.__ref

    def _resolve_ref(self, api_entity):
        self.__obj = api_entity

    def accept(self, visitor):
        if self.__obj is not None:
            self.__obj.accept(visitor)
        else:
            visitor(self)
        return

    def target(self):
        """
        If this ReferenceObject has been resolved, return the targetted object.
        Otherwise, return the reference data, verbatim.

        Returns:
            OpenApiEntity: the target OpenApiEntity, or else {"$ref": "..."}
        """
        if self.__obj is None:
            return self.__data
        else:
            return self.__obj

    def value(self, show_unset=False):
        # TODO: account for cyclical references...
        return self.target().value()


def openapi_is_ref(data):
    """
    Check if a given object is a reference
    """
    if isinstance(data, dict):
        ref_path = data.get("$ref")
        if ref_path:
            if len(data) != 1:
                raise MalformedDocumentException(
                    "ReferenceObjects cannot have more than one key")
            return True
    return False


def openapi_obj_or_ref(data, doc_path, obj_type):
    if openapi_is_ref(data):
        return ReferenceObject(data, doc_path)
    else:
        return obj_type(data, doc_path)
