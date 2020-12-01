"""
OpenApi object field specification object.
"""

from abc import ABC, abstractmethod
from .reference import openapi_obj_or_ref
from .exceptions import (
    MalformedDocumentException,
)


class OpenApiDataSpec(ABC):
    """
    Base object for OpenApi field definitions.
    """

    def __init__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    def parse(self, parent, data):
        """
        Parse this object from raw data.
        """
        field_name, field_val = self._parse(parent, data)
        return field_name, field_val

    @abstractmethod
    def _parse(self, parent, data):
        """
        Subclasses must override to provide parsing functionality.
        """
        pass


class OpenApiFieldSpec(OpenApiDataSpec):
    """
    Field type specification for members of OpenAPI document objects.
    """

    def __init__(self, name, spec_type, default=None):
        super().__init__()
        self.name = name
        self.spec_type = spec_type
        self.__default = default

    def __iter__(self):
        yield self.name

    def _parse(self, parent, data):
        field_val = None
        field_path = "/".join((parent.doc_path, self.name))

        if self.name in data:
            field_val = openapi_obj_or_ref(
                data[self.name], field_path, self.spec_type)
        elif self.__default is not None:
            field_val = self.spec_type(self.__default, field_path)

        return (self.name, field_val)


class OpenApiFieldUnion(OpenApiDataSpec):

    def __init__(self, *args):
        super().__init__()
        self.__fields = args

    def __iter__(self):
        for field in self.__fields:
            for name in iter(field):
                yield name

    def _parse(self, parent, data):
        union_name = None
        union_val = None

        for field in self.__fields:
            field_name, field_val = field.parse(parent, data)

            if field_val is None:
                continue

            if union_val is None:
                union_val = field_val
                union_name = field_name
            else:
                msg = r'fields "{union_name}" and "{field_name}" are mutually exclusive.'
                raise MalformedDocumentException(parent, union_name, msg)

        return union_name, union_val
