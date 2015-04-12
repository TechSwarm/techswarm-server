Feature: Telemetry

  Scenario: Getting telemetry data
    Given following telemetry data
      | timestamp                  | temperature | pressure |
      | 1970-01-01T00:00:00.000000 | 23.6        | 1000     |
      | 2015-04-01T18:53:51.612235 | 24.0        | 1100     |
    When I request /telemetry
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    [
      {"timestamp": "1970-01-01T00:00:00.000000", "temperature": 23.6,
      "pressure": 1000},
      {"timestamp": "2015-04-01T18:53:51.612235", "temperature": 24.0,
      "pressure": 1100}
    ]
    """
    When I request /telemetry?since=2010-04-01T18:53:51.612235
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    [
      {"timestamp": "2015-04-01T18:53:51.612235", "temperature": 24.0,
      "pressure": 1100}
    ]
    """
    When I request /telemetry?since=1970-01-01T00:00:00.000000
    Then 200 status code should be returned
      And the same JSON data should be sent
      # 'since' parameter works like "greater", not "greater than"
    When I request /telemetry?since=2020-04-01T18:53:51.612235
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    []
    """

  Scenario: Adding telemetry data
    When I POST example telemetry data
    Then 201 status code should be returned
      And example telemetry data should be saved to the database

  Scenario Outline: Missing parameters when adding telemetry data
    When I POST example telemetry data without <parameter>
    Then 400 status code should be returned

    Examples:
      | parameter   |
      | timestamp   |
      | temperature |
      | pressure    |
