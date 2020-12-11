"""
OpenApi 3.0 Primitive datatype definitions.

See also:
- https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#data-types
"""

from .entity import OpenApiEntity
from .exceptions import DocumentParsingException

class OpenApiPrimitive(OpenApiEntity):
    """
    Base type for OpenAPI document primitive types.
    The types are as follows:

    +----------+-----------+-----------------------------------+
    | type     | format    | Comments                          |
    +==========+===========+===================================+
    | integer  | int32     | signed 32 bits                    |
    +----------+-----------+-----------------------------------+
    | integer  | int64     | signed 64 bits (a.k.a long)       |
    +----------+-----------+-----------------------------------+
    | number   | float     |                                   |
    +----------+-----------+-----------------------------------+
    | number   | double    |                                   |
    +----------+-----------+-----------------------------------+
    | string   |           |                                   |
    +----------+-----------+-----------------------------------+
    | string   | byte      | base64 encoded characters         |
    +----------+-----------+-----------------------------------+
    | string   | binary    | any sequence of octets            |
    +----------+-----------+-----------------------------------+
    | boolean  |           |                                   |
    +----------+-----------+-----------------------------------+
    | string   | date      | As defined by full-date - RFC3339 |
    +----------+-----------+-----------------------------------+
    | string   | date-time | As defined by date-time - RFC3339 |
    +----------+-----------+-----------------------------------+
    | string   | password  | A hint to UIs to obscure input.   |
    +----------+-----------+-----------------------------------+
    """

    def __init__(self, data, doc_path=None, data_format=None):
        self._value = data
        self._format = data_format
        super().__init__(data, doc_path)

    def _init_data(self, data):
        self._value = data
        pass

    @property
    def format(self):
        return self._format

    def value(self, show_unset=False):
        """
        Subclasses MUST override to provide native python version of
        encapsulated data.
        """
        return self._value

    def validate(self):
        if not isinstance(self._value,self._value_type):
            raise DocumentParsingException(
                    'Error at {}: expected {}; got {}'.format(
                        self.doc_path, self._value_type, type(self._value)))

    def __hash__(self):
        return hash(self._value)

    def __repr__(self):
        return f'{self.__class__.__name__}({repr(self._value)})'

    def __str__(self):
        """
        Return the representation of the encapsulated value.
        """
        return str(self._value)

    def __lt__(self, other):
        if isinstance(other, OpenApiPrimitive):
            return self._value < other._value
        else:
            return self._value < other

    def __le__(self, other):
        if isinstance(other, OpenApiPrimitive):
            return self._value <= other._value
        else:
            return self._value <= other

    def __eq__(self, other):
        """
        OpenApiPrimitives should be considered equal to other if:
         - other is an OpenApiPrimitive encapsulating the same value
         - other is the same type as the encapsulated value and they are equal
        """
        if isinstance(other, OpenApiPrimitive):
            return self._value == other._value
        else:
            return self._value == other

    def __ne__(self, other):
        if isinstance(other, OpenApiPrimitive):
            return self._value != other._value
        else:
            return self._value != other

    def __gt__(self, other):
        if isinstance(other, OpenApiPrimitive):
            return self._value > other._value
        else:
            return self._value > other

    def __ge__(self, other):
        if isinstance(other, OpenApiPrimitive):
            return self._value >= other._value
        else:
            return self._value >= other


class OpenApiInteger(OpenApiPrimitive):
    _value_type = int


class OpenApiNumber(OpenApiPrimitive):
    _value_type = float


class OpenApiString(OpenApiPrimitive):
    _value_type = str


class OpenApiBoolean(OpenApiPrimitive):
    _value_type = bool


class OpenApiAny(OpenApiPrimitive):
    """
    Utility class to wrap ANY type of field value.
    """
    _value_type = object
