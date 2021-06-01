import pytest
from poast.openapi3.spec.document import InfoObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_info():
    return
    c = InfoObject({
    }).validate()
    assert c['field'] == 'val'


def test_info_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        InfoObject({
        }).validate()
