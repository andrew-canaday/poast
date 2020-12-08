import pytest
from poast.openapi3.spec.document import OAuthFlowsObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_oauthflows():
    return
    c = OAuthFlowsObject({
    }).validate()
    assert c['field'] == 'val'


def test_oauthflows_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        OAuthFlowsObject({
        }).validate()
