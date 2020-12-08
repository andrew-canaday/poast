import pytest
from poast.openapi3.spec.document import SchemaObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_schema():
    return
    c = SchemaObject({
    }).validate()
    assert c['field'] == 'val'


def test_schema_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        SchemaObject({
        }).validate()
