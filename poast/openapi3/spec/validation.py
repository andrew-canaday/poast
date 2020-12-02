"""
This module defines validation funcdtions used by the document spec.
"""

import validators
import json

from .model.exceptions import (
    InvalidFieldValueException,
    MissingRequiredFieldException,
)


def require(doc_obj, field_name):
    if doc_obj[field_name] is None:
        raise MissingRequiredFieldException(doc_obj, field_name)
    return


def require_value(doc_obj, field_name, required_val):
    field_val = doc_obj[field_name]
    if field_val and field_val != required_val:
        raise InvalidFieldValueException(
            doc_obj, field_name,
            f'expected: {json.dumps(required_val)}; got: {json.dumps(doc_obj[field_name].value())}')
    return


def required(field_name):
    """
    Decorator used to require that a given field is present.
    """
    def _wrap_func(func):
        def _wrap_self(self):
            if self[field_name] is None:
                require(self, field_name)
            return func(self)
        return _wrap_self
    return _wrap_func


def in_range(field_name, valid):
    """
    Decorator used to ensure that a field has a value from a set range.
    """
    def _wrap_func(func):
        def _wrap_self(self):
            if self[field_name] is not None and self[field_name] not in valid:
                raise InvalidFieldValueException(
                    self, field_name, f'{field_name} must be one of {valid}')
            return func(self)
        return _wrap_self
    return _wrap_func


def is_url(field_name):
    """
    Require that a given field is a url, if present.
    """
    def _wrap_func(func):
        def _wrap_self(self):
            if self[field_name] is not None and not validators.url(
                    str(self[field_name])):
                return
                # TODO: handle relative URL's:
                raise InvalidFieldValueException(
                    self, field_name, 'string value must be a valid url')
            return func(self)
        return _wrap_self
    return _wrap_func


def is_email(field_name):
    """
    Require that a given field is a email, if present.
    """
    def _wrap_func(func):
        def _wrap_self(self):
            if self[field_name] is not None and not validators.email(
                    str(self[field_name])):
                raise InvalidFieldValueException(
                    self, field_name, 'string value must be a valid email')
            return func(self)
        return _wrap_self
    return _wrap_func
