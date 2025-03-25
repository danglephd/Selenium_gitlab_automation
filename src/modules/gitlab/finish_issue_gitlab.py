import os

from .signin_page import gitlabsignin
from ..db import sqlite, firebase_db
from .update_testcase_page import onfinish_update_label_and_return_Query, onfinish_add_desc_and_attach_file

from dotenv import load_dotenv

from ..slack import slack_protocol

try:
  load_dotenv()
  GITLAB_USERNAME = os.environ["GITLAB_USERNAME"]
  GITLAB_PASSWORD = os.environ["GITLAB_PASSWORD"]
  TEST_ISSUE_TEMP = os.environ["TEST_ISSUE_TEMP"]
  TEST_ISSUE_FOLDER_TEMP = os.environ["TEST_ISSUE_FOLDER_TEMP"]
  TEST_ISSUE_DESC_TEMP = os.environ["TEST_ISSUE_DESC_TEMP"]
  TEST_ISSUE_FILE_TEMP = os.environ["TEST_ISSUE_FILE_TEMP"]
  
  SIGN_IN_URL = os.environ["SIGN_IN_URL"]
  
  XM_WEB_FIND_ISSUE_URL = os.environ["XM_WEB_FIND_ISSUE_URL"]
  XM_WEB_V2_FIND_ISSUE_URL = os.environ["XM_WEB_V2_FIND_ISSUE_URL"]
  XM_API_FIND_ISSUE_URL = os.environ["XM_API_FIND_ISSUE_URL"]
  XM_API_V2_FIND_ISSUE_URL = os.environ["XM_API_V2_FIND_ISSUE_URL"]
  XM_LA_FIND_ISSUE_URL = os.environ["XM_LA_FIND_ISSUE_URL"]
  ERP_WEB_FIND_ISSUE_URL = os.environ["ERP_WEB_FIND_ISSUE_URL"]
  ERP_WEB_DEMO_FIND_ISSUE_URL = os.environ["ERP_WEB_DEMO_FIND_ISSUE_URL"]
  ERP_SERVER_FIND_ISSUE_URL = os.environ["ERP_SERVER_FIND_ISSUE_URL"]
  ADMIN_PAGE_FIND_ISSUE_URL = os.environ["ADMIN_PAGE_FIND_ISSUE_URL"]
  ERP_XML_TO_SQL_FIND_ISSUE_URL = os.environ["ERP_XML_TO_SQL_FIND_ISSUE_URL"]
  
  XM_WEB_FIND_TEST_ISSUE_URL = os.environ["XM_WEB_FIND_TEST_ISSUE_URL"]
  XM_WEB_V2_FIND_TEST_ISSUE_URL = os.environ["XM_WEB_V2_FIND_TEST_ISSUE_URL"]
  XM_API_FIND_TEST_ISSUE_URL = os.environ["XM_API_FIND_TEST_ISSUE_URL"]
  XM_API_V2_FIND_TEST_ISSUE_URL = os.environ["XM_API_V2_FIND_TEST_ISSUE_URL"]
  XM_LA_FIND_TEST_ISSUE_URL = os.environ["XM_LA_FIND_TEST_ISSUE_URL"]
  ERP_WEB_FIND_TEST_ISSUE_URL = os.environ["ERP_WEB_FIND_TEST_ISSUE_URL"]
  ERP_WEB_DEMO_FIND_TEST_ISSUE_URL = os.environ["ERP_WEB_DEMO_FIND_TEST_ISSUE_URL"]
  ERP_SERVER_FIND_TEST_ISSUE_URL = os.environ["ERP_SERVER_FIND_TEST_ISSUE_URL"]
  ADMIN_PAGE_FIND_TEST_ISSUE_URL = os.environ["ADMIN_PAGE_FIND_TEST_ISSUE_URL"]
  ERP_XML_TO_SQL_FIND_TEST_ISSUE_URL = os.environ["ERP_XML_TO_SQL_FIND_TEST_ISSUE_URL"]
  
  XM_WEB_NEW_ISSUE_URL = os.environ["XM_WEB_NEW_ISSUE_URL"]
  XM_WEB_V2_NEW_ISSUE_URL = os.environ["XM_WEB_V2_NEW_ISSUE_URL"]
  XM_API_NEW_ISSUE_URL = os.environ["XM_API_NEW_ISSUE_URL"]
  XM_API_V2_NEW_ISSUE_URL = os.environ["XM_API_V2_NEW_ISSUE_URL"]
  XM_LA_NEW_ISSUE_URL = os.environ["XM_LA_NEW_ISSUE_URL"]
  ERP_WEB_NEW_ISSUE_URL = os.environ["ERP_WEB_NEW_ISSUE_URL"]
  ERP_WEB_DEMO_NEW_ISSUE_URL = os.environ["ERP_WEB_DEMO_NEW_ISSUE_URL"]
  ERP_SERVER_NEW_ISSUE_URL = os.environ["ERP_SERVER_NEW_ISSUE_URL"]
  ADMIN_PAGE_NEW_ISSUE_URL = os.environ["ADMIN_PAGE_NEW_ISSUE_URL"]
  ERP_XML_TO_SQL_NEW_ISSUE_URL = os.environ["ERP_XML_TO_SQL_NEW_ISSUE_URL"]

  XM_WEB_PROJECT = os.environ["XM_WEB_PROJECT"]
  XM_WEB_V2_PROJECT = os.environ["XM_WEB_V2_PROJECT"]
  XM_API_PROJECT = os.environ["XM_API_PROJECT"]
  XM_API_V2_PROJECT = os.environ["XM_API_V2_PROJECT"]
  XM_LA_PROJECT = os.environ["XM_LA_PROJECT"]
  ERP_WEB_PROJECT = os.environ["ERP_WEB_PROJECT"]
  ERP_WEB_DEMO_PROJECT = os.environ["ERP_WEB_DEMO_PROJECT"]
  ERP_SERVER_PROJECT = os.environ["ERP_SERVER_PROJECT"]
  ADMIN_PAGE_PROJECT = os.environ["ADMIN_PAGE_PROJECT"]
  ERP_XML_TO_SQL_PROJECT = os.environ["ERP_XML_TO_SQL_PROJECT"]
  
  project_links = [
    # [XM_WEB_V2_FIND_ISSUE_URL, XM_WEB_V2_PROJECT, XM_WEB_V2_NEW_ISSUE_URL],
    # [XM_API_V2_FIND_ISSUE_URL, XM_API_V2_PROJECT, XM_API_V2_NEW_ISSUE_URL],
    [XM_LA_FIND_ISSUE_URL, XM_LA_PROJECT, XM_LA_NEW_ISSUE_URL, XM_LA_FIND_TEST_ISSUE_URL],
    # [ERP_XML_TO_SQL_FIND_ISSUE_URL, ERP_XML_TO_SQL_PROJECT, ERP_XML_TO_SQL_NEW_ISSUE_URL],
    # [ADMIN_PAGE_FIND_ISSUE_URL, ADMIN_PAGE_PROJECT, ADMIN_PAGE_NEW_ISSUE_URL],
    # [XM_WEB_FIND_ISSUE_URL, XM_WEB_PROJECT, XM_WEB_NEW_ISSUE_URL, XM_WEB_FIND_TEST_ISSUE_URL],
    # [XM_API_FIND_ISSUE_URL, XM_API_PROJECT, XM_API_NEW_ISSUE_URL, XM_API_FIND_TEST_ISSUE_URL],
    # [ERP_WEB_FIND_ISSUE_URL, ERP_WEB_PROJECT, ERP_WEB_NEW_ISSUE_URL, ERP_WEB_FIND_TEST_ISSUE_URL],
    [ERP_WEB_DEMO_FIND_ISSUE_URL, ERP_WEB_DEMO_PROJECT, ERP_WEB_DEMO_NEW_ISSUE_URL, ERP_WEB_DEMO_FIND_TEST_ISSUE_URL],
    # [ERP_SERVER_FIND_ISSUE_URL, ERP_SERVER_PROJECT, ERP_SERVER_NEW_ISSUE_URL, ERP_SERVER_FIND_TEST_ISSUE_URL]
  ]

  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except  Exception as error:
  print("Main, Environment variable does not exist: ",  type(error).__name__, "–", error)

def collect_finish_gitlab_issues(issue_finished_list):
    
    # SQLitedb
    criteria = "WHERE test_state LIKE 'Finish'"
    issue_list = sqlite.getListIssue(criteria)

    if len(issue_list) > 0:
      for item in issue_list:
        issue_finished_list.append(item)

def finish_testcase(driver, wait):
    print("RPA finish_testcase")
    issue_finished_list = []
    collect_finish_gitlab_issues(issue_finished_list)
    if(len(issue_finished_list) > 0):
      gitlabsignin(driver, SIGN_IN_URL, GITLAB_USERNAME, GITLAB_PASSWORD)
      for row in issue_finished_list:
        # id, project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url
        onfinish_add_desc_and_attach_file(driver, wait, test_issue_url=row.issue_test_url, project=row.project, test_file_path=row.path)
        query = onfinish_update_label_and_return_Query(driver, wait, issue_url_item=row.issue_url, id=row.id)

        sqlite.executeQuery(query) # Save to db
    slack_protocol.send_survey(user="AAAA", block=slack_protocol.read_blocks([], issue_finished_list, is_finishing=True, is_creating=False), text="Selenium result")