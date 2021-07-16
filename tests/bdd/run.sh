# To run bbd behave with print

# behave -f plain --no-capture

# To run bbd behave with print specific feature

# behave -f plain --no-capture --tags="@file.available"


# behave -f plain --no-capture --tags="@file.not_available"


#behave -f plain --no-capture --tags="@file.deleted"


#behave -f plain --no-capture --tags="@file.not_exist_for_delete"


#behave -f plain --no-capture --tags="@file.create_file_already_exist"


#behave -f plain --no-capture --tags="@file.create_file_with_invalid_data"

behave -f plain --no-capture --tags="@file.update_existing_file"

#behave -f plain --no-capture --tags="@file.update_none_existing_file"


#behave -f plain --no-capture --tags="@file.created_new_file"


