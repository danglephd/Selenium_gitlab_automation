@echo off

call .\Scripts\activate.bat

pytest  .\test\testrpa_finish_testcaseFB.py

pytest  .\test\testrpa_create_testcaseFB.py

exit 0