import pytest
from poast.openapi3.spec.document import PathItemObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_pathitem():
    return
    c = PathItemObject({
    }).validate()
    assert c['field'] == 'val'


def test_pathitem_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        PathItemObject({
        }).validate()
