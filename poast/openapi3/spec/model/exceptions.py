"""
Exception types for OpenApi 3.0 docs
"""


class DocumentParsingException(Exception):
    """
    Exception type thrown when an error is encountered parsing an OpenAPI
    document, which may not be due to a malformed document.
    """
    pass


class MalformedDocumentException(DocumentParsingException):
    """
    Exception type thrown on malformed OpenAPI 3.0 data.
    """
    def __init__(self, doc_obj, field_name, msg):
        self.doc_obj = doc_obj
        self.field_name = field_name
        super().__init__('Error at {}: Field "{}" in {}: {}'.format(
            doc_obj.doc_path, field_name, doc_obj.openapi_type, msg))


class InvalidFieldValueException(MalformedDocumentException):
    pass


class MissingRequiredFieldException(MalformedDocumentException):
    """
    Exception type thrown when a required field is missing from an OpenAPI
    document object
    """

    def __init__(self, doc_obj, field_name):
        super().__init__(doc_obj, field_name, 'is required')
