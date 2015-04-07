Feature: Error handlers

  Scenario: 404 handler
    When I request /lolwtfrandom1337
    Then 404 status code should be returned
      And "error" key in returned JSON data should contain text "Not found"
