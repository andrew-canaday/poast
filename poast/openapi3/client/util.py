"""
General utilities used by poast OpenApiClient generation modules.
"""

import keyword
import string

PATH_ITEM_VERBS = (
    'get', 'put', 'post', 'delete', 'options', 'head', 'patch', 'trace')

CLIENT_RESERVED_KWARGS = set((
    'headers',
    'params',
    'cookies',
    'data',
    'json',
    'files',
    'hooks',
))

CLIENT_PARAM_SUFFIX = '_'


def sanitize_identifier(name, reserved=set(), prefix='', suffix='_'):
    """
    Check to see if the input string is one of:
     - Python reserved keywords
     - Any word from the reserved list

    If so, return a modified version of the parameter which can be safely used.
    """
    if name is None:
        return ''

    if keyword.iskeyword(name) or name in reserved:
        return f'{prefix}{name}{suffix}'
    else:
        return name


def sanitize_fmt_string(fmt_string, reserved=None, prefix='', suffix='_'):
    """
    Check the URI path for:
     - Python reserved keywords
     - Any word from the reserved list

    Reconstitue the format string with offending identifiers adjusted.
    """
    parts = []
    for text, name, spec, conv in string.Formatter().parse(fmt_string):
        parts.append(text)
        name = sanitize_identifier(name, reserved, prefix, suffix)
        if name:
            parts.append('{' + name + '}')
    return ''.join(parts)


def client_sanitize(f, x): return f(
    x, reserved=CLIENT_RESERVED_KWARGS, suffix=CLIENT_PARAM_SUFFIX)
