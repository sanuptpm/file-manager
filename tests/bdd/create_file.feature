Feature: Create file

  @file.new_file_created
  Scenario Outline: successfully create file
    Given get create input <file_name>
    When  create new file
    Then  show create status


    Examples:
      |file_name  |
      |new   |
    Then delete created file

  @file.create_file_already_exist
  Scenario Outline: already created file
    Given already exist create input <file_name>
    When try to create new file with existing file name
    Then already exist create file status


    Examples:
      |file_name  |
      |new   |
    Then delete already created file


  @file.create_file_with_invalid_data
  Scenario Outline: create file with invalid data
    Given get file name input for invalid data <file_name>
    When try to create new file with invalid data
    Then get error status
    Examples:
      | file_name |
      | new       |