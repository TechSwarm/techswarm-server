Feature: Error handlers

  Scenario: 404 handler
    When the user requests /lolwtfrandom1337
    Then 404 error should be returned
      And "error" key should contain text "Not found"
