#!/usr/bin/env python3
import os
from poast.openapi3.spec import OpenApiObject
from poast.openapi3.client import gen_client_cls

# Use swagger.io's petstore example, by default:
PETSTORE_SPEC = 'https://petstore3.swagger.io/api/v3/openapi.json'
PETSTORE_ROOT = 'https://petstore3.swagger.io/api/v3'

# Allow the user to override the spec/root url's:
SPEC_SOURCE = os.environ.get('OPENAPI_SPEC', PETSTORE_SPEC)
API_ROOT_URL = os.environ.get('API_ROOT_URL', PETSTORE_ROOT)

if __name__ == '__main__':
    """
    Demonstrate the basic features of the poast parser/client.
    """
    # Load (and validate!) the spec:
    api_spec = OpenApiObject(SPEC_SOURCE)

    # Create a class that can be used to instantiate clients for this API:
    ApiClient = gen_client_cls('PoastExampleClient', api_spec)

    # Instantiate a client:
    client = ApiClient(PETSTORE_ROOT)

    # Client features:
    help(client)

    # API operations:
    help(client.op)

    # Get the inventory:
    print(f'Inventory:\n{client.op.getInventory().execute().json()}')

    # List a specific pet:
    print(f'Pet #2:\n{client.op.getPetById(petId=2).execute().json()}')
