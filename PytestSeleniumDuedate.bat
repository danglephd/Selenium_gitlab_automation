@echo off

call .\Scripts\activate.bat

pytest  .\test_rpa_gitlab_duedate.py

exit 0