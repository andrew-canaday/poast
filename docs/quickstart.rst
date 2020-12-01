Quickstart
==========


Specs
-----
Loading
^^^^^^^

OpenAPI specifications are loaded using :class:`~poast.openapi3.spec.document.OpenApiObject`.

Specs can be loaded from an :mod:`io` object, a file path, or a URI. Both
``json`` and ``yaml`` files are supported.

First, get the thing imported::

    >>> from poast.openapi3.spec import OpenApiObject

Then, load a spec (all of the following work)::

    >>> doc_from_url = OpenApiObject(
    ...     'https://petstore3.swagger.io/api/v3/openapi.json')

    >>> doc_from_filepath = OpenApiObject('./my/openapi.yml')

    >>> with open('./my/other/openapi.json', 'rb') as f:
    >>>   from_io = OpenApiObject(f)


Validation
^^^^^^^^^^

Validation is performed using the ``validate()`` method on the returned
``OpenApiObject``, e.g.::

    >>> my_doc = OpenApiObject('./path/to/my/openapi.yml')
    >>> my_doc.validate()


- *Loading or validation* errors will raise :class:`~poast.openapi3.spec.model.exceptions.DocumentParsingException`.
- Errors with the *document* itself, will raise :class:`~poast.openapi3.spec.model.exceptions.MalformedDocumentException`

.. seealso:: :mod:`poast.openapi3.spec.model.exceptions`

Clients
-------

Generating
^^^^^^^^^^

Clients are created from a :class:`~poast.openapi3.spec.document.OpenApiObject`
using :func:`~poast.openapi3.client.get_client_cls` function, e.g.::

    >>> from poast.openapi3.spec import OpenApiObject
    >>> from poast.openapi3.client import gen_client_cls
    >>>
    >>> # api_spec = OpenApiObject(...).validate()
    >>>
    >>> # Generate a client class from the spec:
    >>> MyApiClient = gen_client_cls('MyApiClient', api_spec)


The return value is a subclass of :class:`~poast.openapi3.client.basecli.OpenApiClient`,
objects of which can be instantiated in the usual fashion::

    >>> client = MyApiClient('https://myservice.com/api/root')


API Operations
^^^^^^^^^^^^^^

The client classes created using :func:`~poast.openapi3.client.get_client_cls` have
a special attribute, ``op`` (an API-specific subclass of :class:`~poast.openapi3.client.baseop.OpenApiOperations`),
with one method for each `API operation <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#operationObject>`_
defined in the spec. For example, if an api describes two operations,
``someAction`` and ``anotherAction``, client instances will have the following
two methods in their ``op`` object::

    >>> client.op.someAction()
    >>> client.op.anotherAction()

Invoking Operations
"""""""""""""""""""

Methods defined on the ``OpenApiOperations`` subclass generally mimic the
call signature of :func:`requests.Request`, with *path parameters passed as
keyword arguments*.

Request Parameters
..................

+----------------+------------------------+
| Spec ``"in"``: | Passed as:             |
+================+========================+
| ``path``       | ``**kwargs``           |
+----------------+------------------------+
| ``query``      | ``params`` ``(dict)``  |
+----------------+------------------------+
| ``header``     | ``headers`` ``(dict)`` |
+----------------+------------------------+
| ``cookie``     | ``cookies`` ``(dict)`` |
+----------------+------------------------+

Request Body
............
The the `request body <https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#requestBodyObject>`_
can passed - :mod:`requests`-style as either
``json``, ``data``, ``stream``, or ``files``.


.. note::
   In the event that a path parameter collides with a Python keyword, builtin,
   or existing named parameter to the underlying :class:`requests.Request`
   object method, both the URI template and the parameter name are adjusted to
   include the suffix ``'_'``.


Example
^^^^^^^

Consider, for instance, a utility provider which provides a customer API.
Let's suppose that the API provides a ``getUsage`` operation which requires us
to make a ``GET`` request with:

 - a ``customerId`` parameter specified in the URI path
 - a ``days`` parameter, specified as a query arg
 - an auth token, in the ``X-API-Key`` HTTP header

Finding the resource usage for user #123 over the last 30 days might look like::

    >>> resp = my_client.getUsage(
    ...   customerId=123,
    ...   params={'days': 30},
    ...   headers{'X-API-KEY': MY_SECRET_API_KEY}
    ... ).execute()

The ``resp`` object here is a standard :class:`requests.Response` object.
We can get the body as text like so::

    >>> print(resp.text)


Or (if it's JSON), like so::

   >>> print(resp.json())

API Help
^^^^^^^^

Operations for generated clients include docstrings for each method that
indicates the type and location of all required parameters, e.g.::

    >>> help(my_client.op.getPetById)
    Help on method getPetById in module poast.openapi3.client.genop:
    
    getPetById(headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params) method of poast.openapi3.client.genops.PoastExampleClientOperations instance
        http: GET /pet/{petId}
        summary: Find pet by ID
        description: Returns a single pet
    
        path parameters (keyword args):
          petId:
            description: ID of pet to return
            required: True
            deprecated: False
            allowEmptyValue: False
    
        Security Requirements:
          api_key: []
          petstore_auth: ['write:pets', 'read:pets']


Resources
"""""""""

For other examples, see:

 - `example: PetStoreClient <example/help/petstore-client.html>`_
 - `example: PetStoreClient Operations <example/help/petstore-operations.html>`_
