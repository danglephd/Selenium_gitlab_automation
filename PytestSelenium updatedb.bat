@echo off

call .\Scripts\activate.bat

pytest  .\test\testrpa_generate_db.py
exit 0