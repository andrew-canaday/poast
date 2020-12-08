import pytest
from poast.openapi3.spec.document import MediaTypeObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_mediatype():
    return
    c = MediaTypeObject({
    }).validate()
    assert c['field'] == 'val'


def test_mediatype_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        MediaTypeObject({
        }).validate()
