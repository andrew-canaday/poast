"""
Dynamically generate OpenAPI 3.0 operation methods.
"""
from ..spec.document import OperationObject
from .util import (
    CLIENT_RESERVED_KWARGS,
    CLIENT_PARAM_SUFFIX,
    sanitize_identifier,
)
from .genexec import get_op_executor_cls


def get_op_method(cls_name: str, op_id: str, verb: str, uri_path: str, op_obj: OperationObject):
    """
    Given an OperationObject, return a method that will invoke the
    URI given by the OperationObject.
    """
    # Ensure verb is capitalized for display consistency...
    verb = verb.upper()

    # Get the prepared request wrapper class:
    op_req_cls = get_op_executor_cls(cls_name, op_id, verb, uri_path, op_obj)

    # <Client Class>.<operationId> method body:
    def _prepare_request(self, headers=None, params=None, cookies=None,
                         data=None, json=None, files=None, hooks=None,
                         **path_params):
        # Build full URL and fill in path parameters (HACK):
        path_template = self._client._root_url + uri_path
        request_uri = path_template.format(**path_params)

        # Prepare the request:
        r = self._client._request_cls(
            verb.upper(),
            request_uri, headers=headers, params=params, cookies=cookies,
            data=data, json=json, files=files, hooks=hooks)
        pr = self._client._session.prepare_request(r)

        if op_obj['security']:
            for sec_req in op_obj['security']:
                pass

        # Wrap it in an operation request executor and return:
        pr.execute = op_req_cls(self._client._session, pr)
        return pr

    # Update the docs to make the help...helpful:
    _prepare_request.__doc__ = _get_op_docs(verb, uri_path, op_obj)
    _prepare_request.__name__ = op_id
    _prepare_request.__qualname__ = f'{cls_name}.{op_id}'

    # Return our prepared method for addition to the new client class:
    return _prepare_request


def _get_op_docs(verb: str, uri_path: str, op_obj: OperationObject):
    """
    Given an HTTP verb name, API path, and OperationObject, generate the
    python docstring for a method implementing that operation.
    """
    verb = verb.upper()
    param_docs = {
        'path': [],
        'query': [],
        'header': [],
        'cookies': [],
    }

    # Generate docs for individual parameters, and stash them in a dict by type
    for param in op_obj["parameters"]:
        # HACK: get value pointed to by reference, if referenced...
        param = param.target()

        param_in = str(param['in'])
        param_name = str(param['name'])

        # NOTE: we need to ensure that any path parameters can be passed as
        #       keyword arguments to <Client>.<operationId>(...):
        if param_in == 'path':
            param_name = sanitize_identifier(
                param_name, reserved=CLIENT_RESERVED_KWARGS,
                suffix=CLIENT_PARAM_SUFFIX)
        param_docs[param_in].append(f'  {param_name}:')

        for field_name in ('description',):
            if param[field_name] is not None and str(param[field_name]):
                param_docs[param_in].append(
                    f'    {field_name}: {str(param[field_name])}')

        param_docs[param_in].extend([
            f'    required: {str(param["required"])}',
            f'    deprecated: {str(param["deprecated"])}',
            f'    allowEmptyValue: {str(param["allowEmptyValue"])}',
        ])

    # Add basic operation info:
    op_docs = [f'http: {verb} {uri_path}']
    for field_name in ('summary', 'description'):
        if op_obj[field_name] is not None and str(op_obj[field_name]):
            op_docs.append(f'{field_name}: {str(op_obj[field_name])}')

    # Document the parameters, by location:
    for param_in in ('path', 'query', 'header', 'cookies'):
        if not param_docs[param_in]:
            continue

        # Not path parameter usage:
        if param_in == 'path':
            op_docs.append(f'\n{param_in} parameters (keyword args):')
        else:
            op_docs.append(f'\n{param_in} parameters:')
        op_docs.extend(param_docs[param_in])

    # Add security requirements:
    op_security = op_obj['security']
    if op_security:
        op_docs.append('\nSecurity Requirements:')
        for sec_req in op_security:
            if sec_req is None:
                continue

            for name in sec_req:
                op_docs.append(f'  {str(name)}: {sec_req[name].value()}')

    # Return the fully-formed doc string:
    return '\n'.join(op_docs)
