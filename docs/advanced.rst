Advanced Usage
==============

Prepared Requests
-----------------

API operations on :class:`~poast.openpi3.client.baseop.OpenApiOperations`
objects return standard :class:`requests.PreparedRequest` object, patched to
include an ``execute()`` method (an instance of :class:`~poast.openapi3.client.executor.RequestExecutor`).

This allows the client opportunity to make last minute modifications to a
request before it is sent, e.g.::

    >>> req = my_client.someAction()
    >>> # Make some adjustment to the body:
    >>> req.body += r'This has to get appended'

    >>> # Fire it off and get a standard requests.Response:
    >>> resp = req.execute()


Client Configuration
--------------------

.. seealso:: :class:`poast.openapi3.client.config.ClientConfig`.


Custom Sessions
---------------

Using a specific session
""""""""""""""""""""""""
A particular :class:`requests.Session` (or compatible) session instance can be
passed in at the time of client instantiation, using the ``session`` parameter::

    >>> my_session = requests.Session()
    >>> my_client = MyClientClass(root_url='http://something.com',
    ...   session=my_session)


Using a custom class
""""""""""""""""""""
To use a specific *class* of session object for a client::

    >>> my_client = MyClientClass(root_url='http://something.com',
    ...   config=ClientConfig(session_cls=SpecialSessionClass))


Custom Requests
---------------

To use a specific *class* of request object for a client::

    >>> my_client = MyClientClass(root_url='http://something.com',
    ...   config=ClientConfig(request_cls=SpecialRequestClass))


