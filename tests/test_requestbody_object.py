import pytest
from poast.openapi3.spec.document import RequestBodyObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_requestbody():
    return
    c = RequestBodyObject({
    }).validate()
    assert c['field'] == 'val'


def test_requestbody_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        RequestBodyObject({
        }).validate()
