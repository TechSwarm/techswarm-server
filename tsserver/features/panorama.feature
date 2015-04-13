Feature: Panorama photos

  Scenario: No panoramas
    When I request /panorama
    Then 404 status code should be returned
    Given test photos in upload directory
      And following photo data
        | timestamp                  | filename    |
        | 1970-01-01T00:00:00.000000 | test001.jpg |
    When I request /panorama
    Then 404 status code should be returned

  Scenario: Uploaded photos, one panorama
    Given test photos in upload directory
      And following photo data
        | timestamp                  | filename    | is_panorama |
        | 1970-01-01T00:00:00.000000 | test001.jpg | 0           |
        | 1971-01-01T00:00:00.000000 | test002.jpg | 1           |
    When I request /panorama
    Then JSON with image details should be sent
      And "filename" key in JSON data should be equal to "test002.jpg"

  Scenario: Uploaded multiple panoramas
    Given test photos in upload directory
      And following photo data
        | timestamp                  | filename    | is_panorama |
        | 1971-01-01T00:00:00.000000 | test001.jpg | 1           |
        | 2010-01-01T00:00:00.000000 | test002.jpg | 1           |
        | 2000-01-01T00:00:00.000000 | test001.jpg | 1           |
    When I request /panorama
    Then JSON with image details should be sent
      # The one with latest timestamp should be sent, despite the order
      # in the database
      And "filename" key in JSON data should be equal to "test002.jpg"

  Scenario: Uploading a panorama
    When I upload a panorama via PUT to /panorama
    Then 201 status code should be returned
      And JSON with image details should be sent
      And "isPanorama" key in JSON data should be equal to "True"
    When I request /panorama
    Then the same JSON data should be sent
    When I request file from "url" key
    Then 200 status code should be returned
      And Content-Type header should be equal to "image/jpeg"
