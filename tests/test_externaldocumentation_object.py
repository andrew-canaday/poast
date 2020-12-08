import pytest
from poast.openapi3.spec.document import ExternalDocumentationObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_externaldocumentation():
    return
    c = ExternalDocumentationObject({
    }).validate()
    assert c['field'] == 'val'


def test_externaldocumentation_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ExternalDocumentationObject({
        }).validate()
