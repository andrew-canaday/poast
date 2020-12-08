import pytest
from poast.openapi3.spec.document import ParameterObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_parameter():
    return
    c = ParameterObject({
    }).validate()
    assert c['field'] == 'val'


def test_parameter_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        ParameterObject({
        }).validate()
