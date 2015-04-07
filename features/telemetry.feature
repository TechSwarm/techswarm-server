Feature: Telemetry

  Scenario: Getting telemetry data
    Given following telemetry data
      | temperature | pressure |
      | 23.6        | 1000     |
      | 24.0        | 1100     |
    When I request /telemetry
    Then 200 status code should be returned
    And following JSON data should be sent
    """
    [
      {"temperature": 23.6, "pressure": 1000},
      {"temperature": 24.0, "pressure": 1100}
    ]
    """

  Scenario: Adding telemetry data
    When I POST example telemetry data
    Then 201 status code should be returned
    And example telemetry data should be saved to the database

  Scenario Outline: Missing parameters when adding telemetry data
    When I POST example telemetry data without <parameter>
    Then 400 status code should be returned

  Examples: Parameters
    | parameter   |
    | temperature |
    | pressure    |
