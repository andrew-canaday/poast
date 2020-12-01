#!/usr/bin/env python3
import os
from poast.openapi3.spec import OpenApiObject
from poast.openapi3.client import gen_client_cls
from requests_oauthlib import OAuth1Session

TWITTER_SPEC='https://api.twitter.com/labs/2/openapi.json'
TWITTER_ROOT='https://developer.twitter.com/'

if __name__ == '__main__':
    """
    Demonstrate the basic features of the poast parser/client using
    requests-oauthlib.
    """
    # HACK: resolve references because gen_client_cls doesn't handle this
    #       automatially, atm:
    api_spec = OpenApiObject(TWITTER_SPEC, resolve_refs=True)

    ApiClient = gen_client_cls('TwitterClient', api_spec)

    # Instantiate a client:
    twitter_session = OAuth1Session(
            os.environ.get('CLIENT_KEY'),
            client_secret=os.environ.get('CLIENT_SECRET'),
            resource_owner_key=os.environ.get('RESOURCE_OWNER_KEY'),
            resource_owner_secret=os.environ.get('RESOURCE_OWNER_SECRET'))

    client = ApiClient(TWITTER_ROOT, session=twitter_session)
    help(client.op)

