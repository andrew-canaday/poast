import pytest
from poast.openapi3.spec.document import OpenApiObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_openapi():
    return
    c = OpenApiObject({
    }).validate()
    assert c['field'] == 'val'


def test_openapi_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        OpenApiObject({
        }).validate()
