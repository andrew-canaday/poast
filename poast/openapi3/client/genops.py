"""
Dynamically generate OpenAPI 3.0 operations tables.
"""
from .util import (
    PATH_ITEM_VERBS,
    CLIENT_RESERVED_KWARGS,
    CLIENT_PARAM_SUFFIX,
    sanitize_fmt_string,
)
from .genop import get_op_method
from .baseop import OpenApiOperations


def _get_path_ops(cls_name, uri_path, path_item):
    """
    Given a class cls_name, uri path, and PathItemObject, generate a list
    of key/value pairs where key is a method name and value is the function
    body for a method that invokes that endpoint.
    """
    uri_path = sanitize_fmt_string(
        uri_path, reserved=CLIENT_RESERVED_KWARGS, suffix=CLIENT_PARAM_SUFFIX)
    for verb in PATH_ITEM_VERBS:
        op_item = path_item[verb]
        if op_item is None:
            continue

        op_id = str(op_item['operationId'])
        op_fn = get_op_method(cls_name, op_id, verb, uri_path, op_item)
        yield (op_id, op_fn)
    return


def get_op_cls(cli_cls_name, spec):
    """
    Given a new class name and an OpenApiObject spec, generate a class which
    contains all of the operations for the API described by the spec.
    """

    cls_name = cli_cls_name + 'Operations'
    cls_ns = {
        '__doc__': f'API Operations for {cli_cls_name}',
        '__name__': cls_name,
        '__qualname__': f'{cli_cls_name}.{cls_name}',
    }

    for p in spec['paths']:
        for op_id, op_fn in _get_path_ops(cls_name, str(p), spec['paths'][p]):
            cls_ns[op_id] = op_fn

    return type(cls_name, (OpenApiOperations,), cls_ns)
