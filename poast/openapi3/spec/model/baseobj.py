"""
Base class for OpenApi 3.0 "Objects"

For more info, see:
 - https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#format
"""

from abc import abstractmethod
from .entity import OpenApiEntity


class OpenApiBaseObject(OpenApiEntity, dict):
    """
    Base class for OpenAPI specification objects.
    """

    def __init__(self, data, doc_path='#'):
        self._defaults = {}
        OpenApiEntity.__init__(self, data, doc_path)
        return

    def __missing__(self, key):
        """
        If a value is missing from the spec, return the default, as defined
        by the standard, if possible.
        """
        return self._defaults.get(key, None)

    @classmethod
    @abstractmethod
    def _obj_spec(cls):
        """
        Subclasses MUST override to provide a list of specifications for the
        fields in the object.
        """
        pass

    def _field_names(self):
        for spec in self._obj_spec():
            for field_name in spec:
                yield field_name

    def _init_data(self, data):
        if data is None:
            data = {}

        self.extensions = {}
        self._init_fields(data)
        self._init_defaults(self._defaults)
        self._init_extensions(data)
        self._post_init()
        return

    def _init_fields(self, data):
        """
        Initialize each of the fields for this object from the input data.
        """
        # Initialize all the fields to None first, for consistency:
        for field_name in self._field_names():
            self[field_name] = None

        for field in self._obj_spec():
            field_name, field_val = field.parse(self, data)
            if not field_name:
                continue
            self[field_name] = field_val
        return

    def _init_extensions(self, data):
        """
        Find and store OpenAPI extension attributes.
        """
        for k, v in data.items():
            # Skip over non-extension items
            if not k.startswith("x-"):
                continue
            self.extensions[k] = v

    def _init_defaults(self, field_defaults):
        pass

    def _post_init(self):
        pass

    def _validate(self):
        pass

    def accept(self, visitor):
        """
        Depth first traversal, via visitor.

        Args:
            visitor (func): a function that takes a single OpenApiEntity as an argument.
        """

        if not callable(visitor):
            raise ValueError("OpenApiObject visitor must be callable")

        for field_name in self._field_names():
            field_val = self.get(field_name, None)
            if field_val is not None:
                field_val.accept(visitor)
        visitor(self)
        return

    def validate(self):
        self._validate()
        for field_name in self._field_names():
            field_val = self.get(field_name, None)
            if field_val:
                field_val.validate()
        return self

    def value(self, show_unset=False):
        """
        Gnarly (in the bad way) convenience/debug function used to return the
        document as a python dictionary for pprinting and dev validation.
        """
        py_data = {}
        for field_name in self._field_names():
            field_val = self.get(field_name, None)
            if field_val is not None:
                py_val = field_val.value()
            else:
                py_val = None

            if py_val or show_unset:
                py_data[field_name] = py_val
        return py_data
