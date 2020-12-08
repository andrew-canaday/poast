import pytest
from poast.openapi3.spec.document import ComponentsObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_components():
    return
    c = ComponentsObject({
    }).validate()
    assert c['field'] == 'val'


def test_components_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ComponentsObject({
        }).validate()
