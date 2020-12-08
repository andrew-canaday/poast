import pytest
from poast.openapi3.spec.document import ServerObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_server():
    return
    c = ServerObject({
    }).validate()
    assert c['field'] == 'val'


def test_server_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ServerObject({
        }).validate()
