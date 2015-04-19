Feature: Ground station info

  Scenario: Ground station info in random order
    Given following ground station info
      | timestamp                  | latitude | longitude |
      | 2015-06-01T12:00:00.000000 | 20.123   | 89        |
      | 2015-06-01T12:30:03.123822 | 40       | -11.1337  |
      | 2015-06-01T12:13:11.777224 | 60.614   | -33       |
    When I request /gsinfo/current
    # The latest one
    Then "latitude" key in JSON data should be equal to "40.0"

  Scenario: No ground station info
    Given no ground station info in database
    When I request /gsinfo
    Then following JSON data should be sent
    """
    []
    """
    When I request /gsinfo/current
    Then 404 status code should be returned

  Scenario Outline: Setting ground station info without authentication
    When I request <url> via <method>
    Then 401 status code should be returned

    Examples:
    | url             | method |
    | /gsinfo         | POST   |
    | /gsinfo/current | PUT    |

  Scenario Outline: Setting invalid ground station info
    Given I am authenticated
    When I POST following data to /gsinfo
      | timestamp                  | latitude   | longitude   |
      | 2015-06-01T12:13:22.777224 | <latitude> | <longitude> |
    Then 400 status code should be returned
    When I PUT following data to /gsinfo/current
      | timestamp                  | latitude   | longitude   |
      | 2015-06-01T12:13:22.777224 | <latitude> | <longitude> |
    Then 400 status code should be returned

  Examples:
    | latitude | longitude |
    | 0        | -180.0001 |
    | 90.00001 | 30        |
    | lol      | 0         |
    | 0        | wtf       |
    | 100      | 200       |

  Scenario Outline: Sending ground station info
    Given I am authenticated
      And no ground station info in database
    When I POST following data to /gsinfo
      | timestamp                  | latitude   | longitude   |
      | 2015-06-01T12:13:22.777224 | <latitude> | <longitude> |
    Then 201 status code should be returned
    When I request /gsinfo/current
    Then following JSON data should be sent
    """
    {
        "timestamp": "2015-06-01T12:13:22.777224",
        "latitude": <latitude>,
        "longitude": <longitude>
    }
    """
    Given no ground station info in database
    When I PUT following data to /gsinfo/current
      | timestamp                  | latitude   | longitude   |
      | 2015-06-01T12:13:22.777224 | <latitude> | <longitude> |
    Then 201 status code should be returned
    When I request /gsinfo/current
    Then the same JSON data should be sent

  Examples:
    | latitude | longitude |
    | 20       | 40        |
    | 89.99    | -0        |
    | -89.99   | 179.999   |
    | -0       | 0         |

