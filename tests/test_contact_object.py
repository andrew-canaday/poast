import pytest
from poast.openapi3.spec.document import ContactObject
from poast.openapi3.spec.model.exceptions import InvalidFieldValueException

def test_contact():
    contact_name = 'Some Name'
    contact_url = 'https://someplace.tld'
    contact_email = 'somebody@someplace.tld'
    c = ContactObject({
        'name': contact_name,
        'url': contact_url,
        'email': contact_email,
        }).validate()
    assert c['name'] == contact_name
    assert c['url'] == contact_url
    assert c['email'] == contact_email

def test_contact_invalid_email():
    with pytest.raises(InvalidFieldValueException):
        c = ContactObject({
            'name': 'Some name',
            'email': 'invalid email address',
            }).validate()
