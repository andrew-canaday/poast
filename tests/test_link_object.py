import pytest
from poast.openapi3.spec.document import LinkObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_link():
    return
    c = LinkObject({
    }).validate()
    assert c['field'] == 'val'


def test_link_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        LinkObject({
        }).validate()
