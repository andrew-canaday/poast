import pytest
from poast.openapi3.spec.model.exceptions import (
        DocumentParsingException,
        MalformedDocumentException,
        InvalidFieldValueException,
        MissingRequiredFieldException,
        )

from poast.openapi3.spec.validation import (
        require,
        require_value,
        required,
        in_range,
        is_url,
        is_email,
        )


class FakeObject(dict):
    """TODO: replace with mock, etc"""

    def __init__(self, *args, **kwargs):
        self.doc_path = 'test'
        self.openapi_type = 'validation-test-type'
        super().__init__(*args, **kwargs)

    def __getitem__(self, name):
        return self.get(name, None)

    @required('required_field')
    def required_val_fn(self):
        pass

    @in_range('range_field', ('a', 'b', 'c'))
    def in_range_val_fn(self):
        pass

    @is_url('url')
    def url_val_fn(self):
        pass

    @is_email('email')
    def email_val_fn(self):
        pass


def test_require():
    require(FakeObject({'required_field': 'some val'}), 'required_field')

def test_require_fail():
    with pytest.raises(MissingRequiredFieldException):
        require(FakeObject({}), 'required_field')

def test_require_value():
    require_value(
            FakeObject({'required_field': 'correct'}),
            'required_field', 'correct')

def test_require_value_fail():
    with pytest.raises(DocumentParsingException):
        require_value(
                FakeObject({'required_field': 'incorrect'}),
                'required_field', 'correct')

def test_require_value_empty():
    require_value(FakeObject(), 'required_field', 'missing okay')

def test_required():
    obj = FakeObject({'required_field': 'abc'})
    obj.required_val_fn()

def test_required_fail():
    with pytest.raises(DocumentParsingException):
        obj = FakeObject()
        obj.required_val_fn()
        pass

def test_in_range():
    obj = FakeObject({'range_field': 'a'})
    obj.in_range_val_fn()

def test_in_range_no_val():
    obj = FakeObject()
    obj.in_range_val_fn()

def test_in_range_fail():
    with pytest.raises(DocumentParsingException):
        obj = FakeObject({'range_field': 'd'})
        obj.in_range_val_fn()
        pass

def test_is_url():
    obj = FakeObject({'url': 'https://gnu.org/'})
    obj.url_val_fn()

def test_is_url_fail():
    with pytest.raises(DocumentParsingException):
        obj = FakeObject({'url': 'not a real url'})
        obj.url_val_fn()

def test_is_url_blank():
    obj = FakeObject({'url': None})
    obj.url_val_fn()

def test_is_email():
    obj = FakeObject({'email': 'somebody@someplace.tld'})
    obj.email_val_fn()

def test_is_email_fail():
    with pytest.raises(DocumentParsingException):
        obj = FakeObject({'email': 'not a real email'})
        obj.email_val_fn()

def test_is_email_blank():
    obj = FakeObject({'email': None})
    obj.email_val_fn()

