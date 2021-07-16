Feature: Update file

  @file.update_existing_file
  Scenario Outline: update already existing file
    Given get file name for update <file_name>
    And create a file for update
    When update existing file content
    Then show update existing status


    Examples:
      |file_name  |
      |new   |
    Then delete update existing file

  @file.update_none_existing_file
  Scenario Outline: update none existing file
    Given get update none existing file name <file_name>
    When update none existing file
    Then show update status of none existing


    Examples:
      |file_name  |
      |new   |