import pytest
from poast.openapi3.spec.document import SecurityRequirementObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_securityrequirement():
    return
    c = SecurityRequirementObject({
    }).validate()
    assert c['field'] == 'val'


def test_securityrequirement_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        SecurityRequirementObject({
        }).validate()
