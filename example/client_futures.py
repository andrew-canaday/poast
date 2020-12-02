#!/usr/bin/env python3
import os
from poast.openapi3.spec import OpenApiObject
from poast.openapi3.client import gen_client_cls
from requests_futures.sessions import FuturesSession

# Use swagger.io's petstore example, by default:
PETSTORE_SPEC = 'https://petstore3.swagger.io/api/v3/openapi.json'
PETSTORE_ROOT = 'https://petstore3.swagger.io/api/v3'

# Allow the user to override the spec/root url's:
SPEC_SOURCE = os.environ.get('OPENAPI_SPEC', PETSTORE_SPEC)
API_ROOT_URL = os.environ.get('API_ROOT_URL', PETSTORE_ROOT)

if __name__ == '__main__':
    """
    Demonstrate the basic features of the poast parser/client using
    requests-futures.

    WARNING: currently poast uses requests.PreparedRequests, which
             requests-futures does not support. The follow works, but
             isn't actually firing off asynchronously...
    """

    # Load (and validate!) the spec:
    api_spec = OpenApiObject(SPEC_SOURCE)

    # Create a class that can be used to instantiate clients for this API:
    ApiClient = gen_client_cls('PoastExampleClient', api_spec)

    # Instantiate a client:
    my_session = FuturesSession()
    client = ApiClient(PETSTORE_ROOT, session=my_session)

    # Send off some requests asynchronously:
    inventory = client.op.getInventory().execute()
    pet2 = client.op.getPetById(petId=2).execute()

    # Wait for both requests to come back and print 'em:
    print(f'Inventory:\n{inventory.json()}')
    print(f'Pet #2:\n{pet2.json()}')
