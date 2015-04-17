Feature: Mission status

  Scenario: Status data in random order
    Given following status data
      | timestamp                  | phase             |
      | 2015-06-01T12:00:00.000000 | countdown         |
      | 2015-06-01T12:30:03.123822 | ground_operations |
      | 2015-06-01T12:13:11.777224 | descend           |
    When I request /status/current
    # The latest one
    Then "phase" key in JSON data should be equal to "ground_operations"

  Scenario: No status data
    Given no status data in database
    When I request /status
    Then following JSON data should be sent
    """
    []
    """
    When I request /status/current
    Then 404 status code should be returned

  Scenario Outline: Setting invalid phase
    When I POST mission phase <phase> in 'phase' parameter to /status
    Then 400 status code should be returned
    When I PUT mission phase <phase> in 'phase' parameter to /status/current
    Then 400 status code should be returned

    Examples:
      | phase        |
      | lol          |
      | wtf          |
      | total-random |
      | launh        |

  Scenario Outline: Setting phase
    Given no status data in database
    When I POST mission phase <phase> in 'phase' parameter to /status
    Then 201 status code should be returned
    When I request /status/current
    Then "phase" key in JSON data should be equal to "<phase>"
    Given no status data in database
    When I PUT mission phase <phase> in 'phase' parameter to /status/current
    Then 201 status code should be returned
    When I request /status/current
    Then "phase" key in JSON data should be equal to "<phase>"

    Examples:
      | phase              |
      | disconnected       |
      | launch_preparation |
      | countdown          |
      | launch             |
      | descend            |
      | ground_operations  |
      | mission_complete   |
