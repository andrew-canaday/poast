import pytest
from poast.openapi3.spec.document import CallbackObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_callback():
    return
    c = CallbackObject({
    }).validate()
    assert c['field'] == 'val'


def test_callback_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        CallbackObject({
        }).validate()
