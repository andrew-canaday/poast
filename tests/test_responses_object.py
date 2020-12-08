import pytest
from poast.openapi3.spec.document import ResponsesObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_responses():
    return
    c = ResponsesObject({
    }).validate()
    assert c['field'] == 'val'


def test_responses_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ResponsesObject({
        }).validate()
