@echo off

call .\Scripts\activate.bat

pytest  .\test\testrpa_finish_testcase.py

pytest  .\test\testrpa_create_testcase.py

exit 0