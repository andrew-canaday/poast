import pytest
from poast.openapi3.spec.document import XMLObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_xml():
    return
    c = XMLObject({
    }).validate()
    assert c['field'] == 'val'


def test_xml_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        XMLObject({
        }).validate()
