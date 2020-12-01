Poast: Python OAS Toolkit
==========================

**Poast** [#]_ is an `OpenAPI 3.0 specification <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`_
parser and client library for Python.

.. danger::

   This project is still in **alpha**. *Interfaces are subject to change.*

.. toctree::
   :maxdepth: 3
   :hidden:

   quickstart
   advanced
   client
   spec
   coming
   history
   maintainer

Features
^^^^^^^^

 - `OpenAPI 3.0.3 <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>`_ compliant parsing and validation
 - Runtime client generation
 - Utilizes :mod:`requests` for underlying HTTP request/response
 - Compatible with :mod:`requests_futures` and :mod:`requests_oauthlib` sessions

Demo
^^^^

**Creating a client from a spec:**::

    >>> from poast.openapi3.spec import OpenApiObject
    >>> from poast.openapi3.client import gen_client_cls

    >>> # Load the spec (path, io stream, url, or string!)
    >>> api_spec = OpenApiObject(
    ...     'https://petstore3.swagger.io/api/v3/openapi.json')

    >>> # [Optionally, perform validation]
    >>> api_spec.validate()

    >>> # Generate a client class from the spec:
    >>> PetStoreClient = gen_client_cls('PetStoreClient', api_spec)

    >>> # Instantiate a client and start using the API!
    >>> client = PetStoreClient('https://petstore3.swagger.io/api/v3')

    >>> print(client.op.getInventory().execute().json())
    {'approved': 57, 'placed': 100, 'delivered': 50}

    >>> print(client.op.getPetById(petId=2).execute().json())
    {'id': 2, 'category': {'id': 2, 'name': 'Cats'}, 'name': 'Cat 2', 'photoUrls': ['url1', 'url2'], 'tags': [{'id': 1, 'name': 'tag2'}, {'id': 2, 'name': 'tag3'}], 'status': 'sold'}

.. [#] Python OpenAPI Specification Toolkit

