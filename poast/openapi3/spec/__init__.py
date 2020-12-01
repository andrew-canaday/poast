"""OpenAPI 3.0 document loader, parser, and validator.

Resources
.........
 - Specification: https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md
"""

from .model.exceptions import (
    MalformedDocumentException,
    MissingRequiredFieldException,
)

from .document import OpenApiObject

# EOF
