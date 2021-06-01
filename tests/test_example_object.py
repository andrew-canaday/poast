import pytest
from poast.openapi3.spec.document import ExampleObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_example():
    return
    c = ExampleObject({
    }).validate()
    assert c['field'] == 'val'


def test_example_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ExampleObject({
        }).validate()
