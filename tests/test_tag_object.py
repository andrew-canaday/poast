import pytest
from poast.openapi3.spec.document import TagObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_tag():
    return
    c = TagObject({
    }).validate()
    assert c['field'] == 'val'


def test_tag_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        TagObject({
        }).validate()
