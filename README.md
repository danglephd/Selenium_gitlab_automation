# Selenium_gitlab_automation
An project use Selenium to auto generate gitlab test case 

## Update

- Add new column duedate:
```
ALTER TABLE ISSUE DROP COLUMN duedate;

ALTER TABLE ISSUE ADD COLUMN duedate char(50) default ' ';
```


### WHAT THIS PROJECT FOR


1. Help QA to create testcase for IPTP's Gitlab issues automatic
3. Help QA update test issues and original issues automatic


### HOW IT WORKS

1. Migrate DB from FirebaseDB to SQLite DB, update locale database.
 - Query issue data from FirebaseDB
 - For each item compare to SQLite DB, find the differents to update or add new
2. Create new testcase for Gitlab Issues with label Need to test.
 - Signin to Gitlab IPTP
 - For each init project:
    - Open Project search page with label Need to test to Collect 
    - Collect: issue title, issue url, issue number.
    - For each collected issue:
      - Create test issue and test case file
      - Update main issue with: link to created test issue, add label Test case, remove label Need to test
      - Update to SQLiteDB: create new issue with status Create
3. Update to SQLiteDB, the Gitlab Issues with status is Finish.
 - Collect the Gitlab Issues with status is Finish.
 - Signin to Gitlab IPTP
 - For each Gitlab Issue item:
   - Open Gitlab Issue Test's link
   - Add description, add attachment
   - Open Gitlab Issue 's link
   - Add labels: Test Pass, wf:Ready_for_UAT
   - Remove label: wf:QA
   - Update SQLite DB: the Gitlab Issues with status is Finish will be update to Done
4. Migrate DB from SQLite DB to FirebaseDB, update locale database.

# How to run it

## Setup

- Install virtualenv (optional)
```bash
python3 -m virtualenv .   
```
- Init venvironment
```bash
virtualenv venvironment 
```
- If error on use file .ps1, then run:
```bash
set-executionpolicy remotesigned
```
- Activate environment
```bash
Scripts\activate
```
- Install from [requirements.txt](requirements.txt)
```bash
pip install -r requirements.txt
```

## Run
- Run pytest on file [rpa_gitlab_qa.py](rpa_gitlab_qa.py)
```bash
pytest .\rpa_gitlab_qa.py
```


### What is included on this project?

- 🖼️ Libraries:
  * **Selenium**, Selenium with Python [link](https://selenium-python.readthedocs.io/index.html)
  * **PyAutoGUI**, PyAutoGUI’s documentation! [link](https://pyautogui.readthedocs.io/en/latest/)
  * **python-dotenv** python-dotenv [link](https://pypi.org/project/python-dotenv/)
  * **pytest** pytest [link](https://docs.pytest.org/en/7.3.x/)
  * **openpyxl** A Python library to read/write Excel 2010 xlsx/xlsm files [link](https://openpyxl.readthedocs.io/en/stable/)
- 🐋 Database:
  * **SQLite**, SQL database engine [link](https://www.sqlite.org/index.html)
