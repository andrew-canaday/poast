import pytest
from poast.openapi3.spec.document import LicenseObject
from poast.openapi3.spec.model.exceptions import (
    InvalidFieldValueException,
    MissingRequiredFieldException,
)


def test_license():
    license_name = 'Some Name'

    # Confirm absolute and relative URL's:
    for license_url in ('https://someplace.tld', '/some-path/license.txt'):
        l = LicenseObject({
            'name': license_name,
            'url': license_url,
        }).validate()
        assert l['name'] == license_name
        assert l['url'] == license_url


def test_license_missing_name():
    license_url = 'https://someplace.tld'
    with pytest.raises(MissingRequiredFieldException):
        LicenseObject({
            'url': license_url,
        }).validate()


def test_license_invalid_url():
    license_url = 'someplace.tld'
    with pytest.raises(InvalidFieldValueException):
        LicenseObject({
            'name': 'Apache 2.0',
            'url': license_url,
        }).validate()

