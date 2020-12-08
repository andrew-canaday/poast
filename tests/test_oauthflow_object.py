import pytest
from poast.openapi3.spec.document import OAuthFlowObject
from poast.openapi3.spec.model.exceptions import MalformedDocumentException


def test_oauthflow():
    return
    c = OAuthFlowObject({
    }).validate()
    assert c['field'] == 'val'


def test_oauthflow_malformed():
    return
    with pytest.raises(MalformedDocumentException):
        OAuthFlowObject({
        }).validate()
