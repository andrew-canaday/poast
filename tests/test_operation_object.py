import pytest
from poast.openapi3.spec.document import OperationObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_operation():
    return
    c = OperationObject({
    }).validate()
    assert c['field'] == 'val'


def test_operation_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        OperationObject({
        }).validate()
