import pytest
from poast.openapi3.spec.document import EncodingObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_encoding():
    return
    c = EncodingObject({
    }).validate()
    assert c['field'] == 'val'


def test_encoding_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        EncodingObject({
        }).validate()
