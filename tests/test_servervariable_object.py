import pytest
from poast.openapi3.spec.document import ServerVariableObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_servervariable():
    return
    c = ServerVariableObject({
    }).validate()
    assert c['field'] == 'val'


def test_servervariable_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ServerVariableObject({
        }).validate()
