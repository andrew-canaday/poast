import pytest
from poast.openapi3.spec.document import SecuritySchemeObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_securityscheme():
    return
    c = SecuritySchemeObject({
    }).validate()
    assert c['field'] == 'val'


def test_securityscheme_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        SecuritySchemeObject({
        }).validate()
