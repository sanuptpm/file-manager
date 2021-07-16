Feature: Create file

  @file.created_new_file
  Scenario Outline: create new file
    Given accept file name for file creation <file_name>
    When  create new file
    Then  show create file status


    Examples:
      |file_name  |
      |new   |
    Then delete created file

  @file.create_file_already_exist
  Scenario Outline: try to create already existing file
    Given already exist create input <file_name>
    When try to create new file with existing file name
    Then show status for already created file


    Examples:
      |file_name  |
      |new   |
    Then delete already created file


  @file.create_file_with_invalid_data
  Scenario Outline: try to create file with invalid data
    Given get file name for file creation with invalid data <file_name>
    When try to create new file with invalid data
    Then show status
    Examples:
      | file_name |
      | new       |