Feature: Delete file

  @file.deleted
  Scenario Outline: File successfully deleted
    Given get file name for delete <input>
    And create new file for delete
    When delete existing file
    Then show delete file status


    Examples:
      | input         |
      | my            |


  @file.not_exist_for_delete
  Scenario Outline: File not existed
    Given get data for delete file <input>
    When no matching files found for delete
    Then show file not found status for delete

    Examples:
      | input |
      | my_delete    |