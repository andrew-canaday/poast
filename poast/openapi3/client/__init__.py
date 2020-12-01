"""Generate OpenAPI clients from :class:`poast.openapi3.spec.document.OpenApiObject` objects.
"""

from .basecli import OpenApiClient
from .basecfg import ClientConfig
from .genops import get_op_cls


def gen_client_cls(cls_name, spec):
    """
    Generate a client class definition from an OpenAPI 3.0 spec.
    """

    # Generate a class which encapsulates all of our API operations:
    op_cls = get_op_cls(cls_name, spec)

    # Consructor for our new client class:
    def __init__(self, root_url="", config=None, session=None):
        """
        Initialize the client with the given root_url and optional config.
        """
        OpenApiClient.__init__(self, root_url, config, session)

        # Install our dynamically generated API operations:
        self.op = op_cls(self)
        return

    # Update qualname to make help() more helpful!
    __init__.__qualname__ = f'{cls_name}.__init__'

    # Configure the class namespace:
    cls_ns = {
        '__doc__': _get_cls_docs(spec),
        '__init__': __init__,
        '__slots__': (
            '__weakref__',
            'op',
        ),
    }

    # Create and return our new API class!
    return type(cls_name, (OpenApiClient,), cls_ns)


def _get_cls_docs(spec):
    """
    Given an OpenApiObject representing a spec, return the doc string for a
    client class for that API.
    """

    # Start with the basics:
    cls_docs = [
        f'API client for "{str(spec["info"]["title"])}" version: {str(spec["info"]["version"])}',
    ]

    # If the API has a description, let's add it!
    if spec["info"]["description"] is not None and str(spec["info"]["description"]):
        cls_docs.append('\nAPI Description:')
        cls_docs.append(str(spec["info"]["description"]))

    return '\n'.join(cls_docs)
