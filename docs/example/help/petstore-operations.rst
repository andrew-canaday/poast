:orphan:

Help: PetStoreClient Operations
===============================

**help(client.op)**::

    class PoastExampleClientOperations(poast.openapi3.client.baseop.OpenApiOperations)
     |  PoastExampleClientOperations(client)
     |
     |  API Operations for PoastExampleClient
     |
     |  Method resolution order:
     |      PoastExampleClientOperations
     |      poast.openapi3.client.baseop.OpenApiOperations
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  addPet(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /pet
     |      summary: Add a new pet to the store
     |      description: Add a new pet to the store
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  createUser(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /user
     |      summary: Create user
     |      description: This can only be done by the logged in user.
     |
     |  createUsersWithListInput(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /user/createWithList
     |      summary: Creates list of users with given input array
     |      description: Creates list of users with given input array
     |
     |  deleteOrder(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: DELETE /store/order/{orderId}
     |      summary: Delete purchase order by ID
     |      description: For valid response try integer IDs with value < 1000. Anything above 1000 or nonintegers will generate API errors
     |
     |      path parameters (keyword args):
     |        orderId:
     |          description: ID of the order that needs to be deleted
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  deletePet(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: DELETE /pet/{petId}
     |      summary: Deletes a pet
     |
     |      path parameters (keyword args):
     |        petId:
     |          description: Pet id to delete
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      header parameters:
     |        api_key:
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  deleteUser(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: DELETE /user/{username}
     |      summary: Delete user
     |      description: This can only be done by the logged in user.
     |
     |      path parameters (keyword args):
     |        username:
     |          description: The name that needs to be deleted
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  findPetsByStatus(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /pet/findByStatus
     |      summary: Finds Pets by status
     |      description: Multiple status values can be provided with comma separated strings
     |
     |      query parameters:
     |        status:
     |          description: Status values that need to be considered for filter
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  findPetsByTags(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /pet/findByTags
     |      summary: Finds Pets by tags
     |      description: Multiple tags can be provided with comma separated strings. Use tag1, tag2, tag3 for testing.
     |
     |      query parameters:
     |        tags:
     |          description: Tags to filter by
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  getInventory(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /store/inventory
     |      summary: Returns pet inventories by status
     |      description: Returns a map of status codes to quantities
     |
     |      Security Requirements:
     |        api_key: []
     |
     |  getOrderById(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /store/order/{orderId}
     |      summary: Find purchase order by ID
     |      description: For valid response try integer IDs with value <= 5 or > 10. Other values will generated exceptions
     |
     |      path parameters (keyword args):
     |        orderId:
     |          description: ID of order that needs to be fetched
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  getPetById(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /pet/{petId}
     |      summary: Find pet by ID
     |      description: Returns a single pet
     |
     |      path parameters (keyword args):
     |        petId:
     |          description: ID of pet to return
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        api_key: []
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  getUserByName(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /user/{username}
     |      summary: Get user by user name
     |
     |      path parameters (keyword args):
     |        username:
     |          description: The name that needs to be fetched. Use user1 for testing.
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  loginUser(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /user/login
     |      summary: Logs user into the system
     |
     |      query parameters:
     |        username:
     |          description: The user name for login
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |        password:
     |          description: The password for login in clear text
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  logoutUser(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: GET /user/logout
     |      summary: Logs out current logged in user session
     |
     |  placeOrder(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /store/order
     |      summary: Place an order for a pet
     |      description: Place a new order in the store
     |
     |  updatePet(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: PUT /pet
     |      summary: Update an existing pet
     |      description: Update an existing pet by Id
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  updatePetWithForm(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /pet/{petId}
     |      summary: Updates a pet in the store with form data
     |
     |      path parameters (keyword args):
     |        petId:
     |          description: ID of pet that needs to be updated
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      query parameters:
     |        name:
     |          description: Name of pet that needs to be updated
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |        status:
     |          description: Status of pet that needs to be updated
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |
     |  updateUser(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: PUT /user/{username}
     |      summary: Update user
     |      description: This can only be done by the logged in user.
     |
     |      path parameters (keyword args):
     |        username:
     |          description: name that need to be deleted
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |  uploadFile(self, headers=None, params=None, cookies=None, data=None, json=None, files=None, hooks=None, **path_params)
     |      http: POST /pet/{petId}/uploadImage
     |      summary: uploads an image
     |
     |      path parameters (keyword args):
     |        petId:
     |          description: ID of pet to update
     |          required: True
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      query parameters:
     |        additionalMetadata:
     |          description: Additional Metadata
     |          required: False
     |          deprecated: False
     |          allowEmptyValue: False
     |
     |      Security Requirements:
     |        petstore_auth: ['write:pets', 'read:pets']
     |


