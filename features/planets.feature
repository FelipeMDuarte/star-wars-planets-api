
Feature: Planets api

  Scenario: Add a new planet
      Given I create a mongodb mock object
      Given json body
      """
      {
      	"name":"endor",
      	"terrain": "TERRAIN EXAMPLE",
      	"climate": "climate example"
      }
      """
      When post request to api/planets is made with starwars api mock
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "code": 200,
        "message": "Cadastro realizado com sucesso",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Add a planet - wrong keys
      Given I create a mongodb mock object
      Given json body
      """
      {
        "nome":"endor",
        "terreno": "TERRAIN EXAMPLE",
        "clima": "climate example"
      }
      """
      When post request to api/planets is made with starwars api mock
      Then the response should have status code 400 BAD REQUEST
      Then the response should have body
      """
      {
        "error_code": "IOE001",
        "message": "Os dados inseridos são inválidos para essa operação.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Add a planet - duplicated entry
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain Example",
        "climate": "Climate Example"
      }
      """
      Given json body
      """
      {
        "name":"endor",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When post request to api/planets is made with starwars api mock
      Then the response should have status code 500 CONFLICT
      Then the response should have body
      """
      {
        "error_code": "GUE000",
        "message": "Erro no serviço star-wars-planets-api: Esse planeta já está cadastrado.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Get list of planets
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given I save a job json in the mongodb
      """
      {
        "name":"Naboo",
        "terrain": "Terrain 2",
        "climate": "Climate 2",
        "films": 3
      }
      """
      When get request to api/planets is made
      Then the response should have status code 200 OK
      Then the response should have body
      """
      [{
        "name": "Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }, {
        "name": "Naboo",
        "terrain": "Terrain 2",
        "climate": "Climate 2",
        "films": 3
      }]
      """
      Then I reset the mongodb mock object

  Scenario: Get list of planets - no planets saved
      Given I create a mongodb mock object
      When get request to api/planets is made
      Then the response should have status code 200 OK
      Then the response should have body
      """
      []
      """
      Then I reset the mongodb mock object

  Scenario: Get a planet by name
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      When get request to api/planets/Endor is made
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "name": "Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Then I reset the mongodb mock object

  Scenario: Get a planet by name - no planet found
      Given I create a mongodb mock object
      When get request to api/planets/Endor is made
      Then the response should have status code 500 INTERNAL ERROR
      Then the response should have body
      """
      {
        "error_code": "GUE000",
        "message": "Erro no serviço star-wars-planets-api: Nenhum planeta foi encontrado.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Get a planet by id
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      When get request to api/planets/ is made getting _id from context
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "name": "Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Then I reset the mongodb mock object

  Scenario: Get a planet by id - no planet found
      Given I create a mongodb mock object
      When get request to api/planets/ is made getting _id from context
      Then the response should have status code 500 INTERNAL ERROR
      Then the response should have body
      """
      {
        "error_code": "GUE000",
        "message": "Erro no serviço star-wars-planets-api: Nenhum planeta foi encontrado.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by name
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given json body
      """
      {
        "name":"Naboo",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/endor is made with starwars api mock
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "code": 200,
        "message": "Update realizado com sucesso",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by name - no planet found
      Given I create a mongodb mock object
      Given json body
      """
      {
        "name":"Naboo",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/endor is made with starwars api mock
      Then the response should have status code 404 NOT FOUND
      Then the response should have body
      """
      {
        "code": 404,
        "message": "O planeta enviado nao foi encontrado: endor",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by name - wrong keys
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given json body
      """
      {
        "nome":"Naboo",
        "terreno": "TERRAIN EXAMPLE",
        "clima": "climate example"
      }
      """
      When put request to api/planets/endor is made with starwars api mock
      Then the response should have status code 400 BAD REQUEST
      Then the response should have body
      """
      {
        "error_code": "IOE001",
        "message": "Os dados inseridos são inválidos para essa operação.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by name - duplicated entry
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 1",
        "films": 1
      }
      """
      Given I save a job json in the mongodb
      """
      {
        "name":"Naboo",
        "terrain": "Terrain 2",
        "climate": "Climate 2",
        "films": 4
      }
      """
      Given json body
      """
      {
        "name":"Naboo",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/endor is made with starwars api mock
      Then the response should have status code 500 INTERNAL ERROR
      Then the response should have body
      """
      {
        "error_code": "GUE000",
        "message": "Erro no serviço star-wars-planets-api: Esse planeta já está cadastrado.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by id
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given json body
      """
      {
        "name":"Naboo",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/ is made getting _id from context
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "code": 200,
        "message": "Update realizado com sucesso",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by id - no planet found
      Given I create a mongodb mock object
      Given json body
      """
      {
        "name":"Naboo",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/ is made getting _id from context
      Then the response should have status code 404 OK
      Then the response should have body
      """
      {
        "code": 404,
        "message": "O planeta enviado nao foi encontrado: 000000000000000000000000",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by id - wrong keys
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given json body
      """
      {
        "nome":"Naboo",
        "terrenno": "TERRAIN EXAMPLE",
        "clima": "climate example"
      }
      """
      When put request to api/planets/ is made getting _id from context
      Then the response should have status code 400 BAD REQUEST
      Then the response should have body
      """
      {
        "error_code": "IOE001",
        "message": "Os dados inseridos são inválidos para essa operação.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Update a planet by id - duplicated entry
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      Given json body
      """
      {
        "name":"Endor",
        "terrain": "TERRAIN EXAMPLE",
        "climate": "climate example"
      }
      """
      When put request to api/planets/ is made getting _id from context
      Then the response should have status code 500 INTERNAL ERROR
      Then the response should have body
      """
      {
        "error_code": "GUE000",
        "message": "Erro no serviço star-wars-planets-api: Esse planeta já está cadastrado.",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Delete a planet by name
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      When delete request to api/planets/Endor is made
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "code": 200,
        "message": "Delete realizado com sucesso",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Delete a planet by name - no planet found
      Given I create a mongodb mock object
      When delete request to api/planets/Endor is made
      Then the response should have status code 404 NOT FOUND
      Then the response should have body
      """
      {
        "code": 404,
        "message": "O planeta enviado nao foi encontrado: Endor",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Delete a planet by id
      Given I create a mongodb mock object
      Given I save a job json in the mongodb
      """
      {
        "name":"Endor",
        "terrain": "Terrain 1",
        "climate": "Climate 2",
        "films": 1
      }
      """
      When delete request to api/planets/ is made getting _id from context
      Then the response should have status code 200 OK
      Then the response should have body
      """
      {
        "code": 200,
        "message": "Delete realizado com sucesso",
        "response": ""
      }
      """
      Then I reset the mongodb mock object

  Scenario: Delete a planet by id - no planet found
      Given I create a mongodb mock object
      When delete request to api/planets/ is made getting _id from context
      Then the response should have status code 404 BAD REQUEST
      Then the response should have body
      """
      {
        "code": 404,
        "message": "O planeta enviado nao foi encontrado: 000000000000000000000000",
        "response": ""
      }
      """
      Then I reset the mongodb mock object
