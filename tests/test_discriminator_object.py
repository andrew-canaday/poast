import pytest
from poast.openapi3.spec.document import DiscriminatorObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_discriminator():
    return
    c = DiscriminatorObject({
    }).validate()
    assert c['field'] == 'val'


def test_discriminator_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        DiscriminatorObject({
        }).validate()
