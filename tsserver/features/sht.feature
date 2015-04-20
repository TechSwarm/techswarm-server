Feature: Humidity-Temperature data

  Scenario: Getting SHT data
    Given following SHT data
      | timestamp                  | humidity | temperature |
      | 1970-01-01T00:00:00.000000 | 70       | 23.6        |
      | 2015-04-01T18:53:51.612235 | 60.5     | 24.0        |
    When I request /sht
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    [
      {"timestamp": "1970-01-01T00:00:00.000000",
      "humidity": 70,
      "temperature": 23.6},
      {"timestamp": "2015-04-01T18:53:51.612235",
      "humidity": 60.5,
      "temperature": 24.0}
    ]
    """
    When I request /sht?since=2010-04-01T18:53:51.612235
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    [
      {"timestamp": "2015-04-01T18:53:51.612235",
      "humidity": 60.5,
      "temperature": 24.0}
    ]
    """
    When I request /sht?since=1970-01-01T00:00:00.000000
    Then 200 status code should be returned
      And the same JSON data should be sent
      # 'since' parameter works like "greater", not "greater than"
    When I request /sht?since=2020-04-01T18:53:51.612235
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    []
    """

  Scenario: Adding data without authentication
    When I request /sht via POST
    Then 401 status code should be returned

  Scenario: Adding SHT data
    Given I am authenticated
    When I POST example SHT data
    Then 201 status code should be returned
      And example SHT data should be saved to the database

  Scenario Outline: Missing parameters when adding SHT data
    Given I am authenticated
    When I POST example SHT data without <parameter>
    Then 400 status code should be returned

    Examples:
      | parameter   |
      | timestamp   |
      | humidity    |
      | temperature |
