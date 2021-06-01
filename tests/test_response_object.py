import pytest
from poast.openapi3.spec.document import ResponseObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_response():
    return
    c = ResponseObject({
    }).validate()
    assert c['field'] == 'val'


def test_response_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ResponseObject({
        }).validate()
