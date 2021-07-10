Feature: List all files
  @file.available
  Scenario: Files are available
    Given searching for file listing
    When get all matching files
    Then show all file name

  @file.not_available
  Scenario: Files are not available
    Given searching for file listing
    When no matching files found
    Then nothing will show