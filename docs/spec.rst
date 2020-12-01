========
Spec API
========


Object Interface
^^^^^^^^^^^^^^^^

All fields in OAS 3.0 objects are accessed using python's ``[]`` operator. This
is done to avoid any confusion between which fields are in the spec vs
attributes of the implementation class and to avoid workarounds wherein spec
fields which conflict with keywords or builtins - e.g. ``in`` - can retain
their original names.

For example, accessing the ``paths`` field in a document is done like so::

    my_doc = OpenApiObject(...)
    paths = my_doc['paths']


OpenApiBaseObject
^^^^^^^^^^^^^^^^^

.. autoclass:: poast.openapi3.spec.model.baseobj.OpenApiBaseObject
    :members:
    :special-members:
    :no-undoc-members:
    :show-inheritance:


Primitive Types
^^^^^^^^^^^^^^^
.. automodule:: poast.openapi3.spec.model.primitives


Container Types
^^^^^^^^^^^^^^^
.. automodule:: poast.openapi3.spec.model.containers


Document Objects
^^^^^^^^^^^^^^^^
.. automodule:: poast.openapi3.spec.document
    :members:

