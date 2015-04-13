Feature: Error handlers

  Scenario: 404 handler
    When I request /lolwtfrandom1337
    Then 404 status code should be returned
      And "message" key in JSON data should be equal to "Not found"
