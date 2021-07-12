Feature: Update file

  @file.update_existing_file
  Scenario Outline: update already existing file
    Given get update file name <file_name>
    When  update existing file
    Then  show update existing status


    Examples:
      |file_name  |
      |new   |
    Then delete update existing file

  @file.update_none_existing_file
  Scenario Outline: update none existing file
    Given get update none existing file name <file_name>
    When  update none existing file
    Then  show update status of none existing


    Examples:
      |file_name  |
      |new   |