import pytest
from poast.openapi3.spec.document import HeaderObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_header():
    return
    c = HeaderObject({
    }).validate()
    assert c['field'] == 'val'


def test_header_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        HeaderObject({
        }).validate()
