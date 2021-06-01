"""
This module defines the OpenApi 3.0 container types

For more info, see:
 - https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#format
"""

from abc import abstractmethod
from .entity import OpenApiEntity
from .reference import openapi_obj_or_ref


class OpenApiContainer(OpenApiEntity):
    def __init__(self, data, doc_path, item_type):
        self._item_type = item_type
        super().__init__(data, doc_path)
        return

    def _init_data(self, data):
        if not isinstance(data, self._container_type):
            raise ValueError(f'Expected {str(self._container_type)}')
        self._init_items(data)
        return

    @abstractmethod
    def _init_items(self, data):
        pass

    def _validate(self):
        pass

    @classmethod
    def of(cls, item_type):
        return lambda data, doc_path: cls(data, doc_path, item_type)


class OpenApiList(OpenApiContainer, list):

    _container_type = list

    def _init_items(self, data):
        for i, e in enumerate(data):
            item_path = f'{self.doc_path}[{i}]'
            item_val = openapi_obj_or_ref(e, item_path, self._item_type)
            self.append(item_val)
        return

    def accept(self, visitor):
        for e in self:
            e.accept(visitor)
        visitor(self)
        return

    def validate(self):
        for i in self:
            if i is not None:
                i.validate()
        self._validate()
        return

    def value(self, show_unset=False):
        return [x.value() for x in self]


class OpenApiMap(OpenApiContainer, dict):

    _container_type = dict

    def _init_items(self, data):
        for k, v in data.items():
            # HACK: I don't think these occur in valid specs, but in case
            # there are references to a map key which contains a slash, we
            # just use container notation:
            if k.find('/') != -1:
                item_path = f'{self.doc_path}["{k}"]'
            else:
                item_path = '/'.join((self.doc_path, k.lstrip('/')))
            item_val = openapi_obj_or_ref(v, item_path, self._item_type)
            self[k] = item_val

    def accept(self, visitor):
        for e in self.values():
            e.accept(visitor)
        visitor(self)
        return

    def validate(self):
        for v in self.values():
            if v is not None:
                v.validate()
        self._validate()

    def value(self, show_unset=False):
        return {k: v.value() for (k, v) in self.items()}
