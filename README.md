<img align="right" height="100" width="100" valign="middle" src="./docs/img/poast-logo-100.png">

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE.md)
[![Build Status](https://travis-ci.com/andrew-canaday/poast.svg?branch=main)](https://travis-ci.com/andrew-canaday/poast)
[![Read the Docs](https://readthedocs.org/projects/poast/badge/?version=latest)](https://poast.readthedocs.io)

Poast
=====

Poast is an [OpenAPI 3.0](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md)
parser/validator and runtime client generator.

> :warning: **WARNING**: _This package is still in **alpha**_.
> (It doesn't even have unit tests yet, folks).


Features
--------

 - [OpenAPI 3.0.3](https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md>) compliant parsing and validation
 - Runtime client generation
 - Utilizes [`requests`](https://github.com/psf/requests) for underlying HTTP request/response handling
 - Compatible with [`requests_futures`](https://github.com/ross/requests-futures) and [`requests_oauthlib`](https://github.com/requests/requests-oauthlib) sessions

### Example

```Python
from poast.openapi3.spec import OpenApiObject
from poast.openapi3.client import gen_client_cls

# Load the spec (path, io stream, url, or string!)
api_spec = OpenApiObject(
    'https://petstore3.swagger.io/api/v3/openapi.json')

# Optionally, perform validation:
api_spec.validate()

# Generate a client class from the spec:
PetStoreClient = gen_client_cls('PetStoreClient', api_spec)

client = PetStoreClient('https://petstore3.swagger.io/api/v3')

# Start using the API!
print(client.op.getInventory().execute().json())
print(client.op.getPetById(petId=2).execute.json())
```

