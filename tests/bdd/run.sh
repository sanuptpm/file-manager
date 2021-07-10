# To run bbd behave with print

# behave -f plain --no-capture

# To run bbd behave with print specific feature

#behave -f plain --no-capture --tags="@file.available"


behave -f plain --no-capture --tags="@file.not_available"

