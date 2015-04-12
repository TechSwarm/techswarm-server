Feature: Photos

  Scenario: Retrieving uploaded photo details
    Given test photos in upload directory
      And following photo data
        | timestamp                  | filename    |
        | 1970-01-01T00:00:00.000000 | test001.jpg |
        | 2015-04-02T12:51:31.127377 | test002.jpg |
    When I request /photos
    Then 200 status code should be returned
      And list of 2 objects with image details should be sent
    When I request /photos?since=1970-01-01T00:00:00.000000
    Then 200 status code should be returned
      And list of 1 object with image details should be sent
    When I request /photos?since=2010-12-02T12:42:11.111111
    Then 200 status code should be returned
      And list of 1 object with image details should be sent
    When I request /photos?since=2050-01-11T11:22:33.444444
    Then 200 status code should be returned
      And following JSON data should be sent
    """
    []
    """

  Scenario: Uploading a photo
    When I upload an image to /photos
    Then 201 status code should be returned
      And JSON with image details should be sent
    When I request file from "url" key
    Then 200 status code should be returned
      And Content-Type header should be equal to "image/jpeg"

  # Depends on config, but you are not going to allow uploading photos with
  # .php extension, are you?
  Scenario Outline: Uploading a file with dangerous extension
    When I upload a file with '<extension>' extension to /photos
    Then 400 status code should be returned
      And "error" key in returned JSON data should contain text "File extension is not allowed!"

  Examples:
    | extension |
    | php       |
    | exe       |
    | py        |
    | rb        |
    | sh        |
