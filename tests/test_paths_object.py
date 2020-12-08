import pytest
from poast.openapi3.spec.document import PathsObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_paths():
    return
    c = PathsObject({
    }).validate()
    assert c['field'] == 'val'


def test_paths_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        PathsObject({
        }).validate()
