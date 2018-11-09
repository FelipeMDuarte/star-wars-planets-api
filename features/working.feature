Feature: Working service feature

  Scenario Outline: Method not Allowed
    When <method> request to api/working is made
    Then should return status code 405 METHOD NOT ALLOWED

      Examples: Methods
          | method |
          | delete |
          | put	   |
          | post   |


  Scenario: mvp-autometadata-jobdata service is not working - MongoDB is down
    When get request to api/working is made
    Then should return status code 200 OK
    Then should have response body
    """
    [
      {
          "service": "mongo-db",
          "status": "error",
          "error_description": "Database timeout.",
          "error_code": "DBE001"
      }
    ]
    """

  Scenario: mvp-autometadata-jobdata service is working
    Given I mock pymongo healthcheck
    When get request to api/working is made
    Then should return status code 200 OK
    Then the return job json matches
    """
    [
      {
          "service": "mongo-db",
          "status": "working",
          "error_description": "",
          "error_code": ""
      }
    ]
    """
    Then I reset pymongo mock
