# To run application
$ python3 app.py
$ python3 src/main.py

# To run unittest with console
$ pytest -s -v
$ pytest  -v -s tests/unittest/

# To run unittest
$ pytest

# get test report 
$ pytest --cov-report term-missing --cov=app test_app.py

# To set PYTHONPATH to import data from other package
$ export PYTHONPATH=/home/sam/Desktop/file-manager

# Create __init_.py file to directory to make as python directory
#to run bdd
$ behave

# to run bdd with print 
$ behave -f plain --no-capture
$ ./run.sh 
