Feature: Delete file

  @file.deleted
  Scenario Outline: File successfully deleted
    Given get delete input <input>
    When create delete file
    Then delete file


    Examples:
      | input         |
      | my            |


  @file.not_exist_for_delete
  Scenario Outline: File not existed
    Given get delete file name <input>
    When no matching files found for delete
    Then show file not found status for delete

    Examples:
      | input |
      | my_delete    |