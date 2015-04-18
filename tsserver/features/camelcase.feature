Feature: Snake case to camel case
  Snake case to camel case conversion is used to output key names out of
  column names in JSON (in Model class' serialize method).

  Please note that since the feature is intended to be used with column names
  which does not have underscores at the beginning, it may not work properly
  with such strings.

  Scenario Outline: Converting snake case strings to camel case
    When I convert <Snake case> to camel case
    Then <Camel case> should be returned

  Examples:
    | Snake case             | Camel case          |
    | test                   | test                |
    | alreadyCamelCase       | alreadyCamelCase    |
    | text_with_underscores  | textWithUnderscores |
    | multiple___underscores | multipleUnderscores |
