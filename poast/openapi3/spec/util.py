"""
poast misc utilities.
"""

import os
import yaml
from urllib.parse import urlparse
from urllib.request import urlopen


def load_yaml(y_src):
    """
    Load a yaml file from a file, path, stream, or url.
    (Returns data as-is, if it's a dict or list).
    """
    # If we get a loaded object, just return the thing:
    if isinstance(y_src, dict) or isinstance(y_src, list):
        return y_src

    # If the input is a string, assume URL or filepath:
    if isinstance(y_src, str) or isinstance(y_src, bytes):
        # If http/https, urlopen and load from there:
        parsed = urlparse(y_src)
        if parsed.scheme in ('http', 'https'):
            return yaml.safe_load(urlopen(y_src))

        # If the path exists, try to load it:
        if os.path.exists(y_src):
            with open(y_src, 'rb') as f:
                return yaml.safe_load(f)

        # Otherwise, assume maybe it's raw input:
        return yaml.safe_load(y_src)

    # Otherwise, assume a stream:
    return yaml.safe_load(f)
