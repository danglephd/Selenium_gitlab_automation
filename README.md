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

## Setup on Ubuntu

- Install Python virtual-environment support (one time)
```bash
sudo apt update
sudo apt install python3.12-venv
```
- Create a virtual environment
```bash
python3 -m venv .venv
```
- Install dependencies
```bash
./.venv/bin/python -m pip install -r requirements.txt
```
- Create a local `.env` file with the GitLab, project URL, template path, Slack,
  and Firebase settings used by the workflow. Do not commit this file or the
  Firebase service-account JSON file.
- Make the Ubuntu scripts executable
```bash
chmod +x PytestSelenium*.sh
```

## Run
- Run all create/finish jobs
```bash
./PytestSelenium.sh
```
- Collect new issues only
```bash
./PytestSelenium_collect_issue.sh
```
- Finish issues only
```bash
./PytestSelenium_Finish.sh
```
- Update the local database
```bash
./PytestSelenium_updatedb.sh
```
- Run the due-date test
```bash
./PytestSeleniumDuedate.sh
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
