import os
from .signin_page import gitlabsignin
from .find_issue_page import get_gitlab_issue_info
from .update_testcase_page import oncreate_testcase_update_issue_update_db
from ..db import firebase

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
    [XM_WEB_FIND_ISSUE_URL, XM_WEB_PROJECT, XM_WEB_NEW_ISSUE_URL, XM_WEB_FIND_TEST_ISSUE_URL],
    [XM_API_FIND_ISSUE_URL, XM_API_PROJECT, XM_API_NEW_ISSUE_URL, XM_API_FIND_TEST_ISSUE_URL],
    [ERP_WEB_FIND_ISSUE_URL, ERP_WEB_PROJECT, ERP_WEB_NEW_ISSUE_URL, ERP_WEB_FIND_TEST_ISSUE_URL],
    # [ERP_WEB_DEMO_FIND_ISSUE_URL, ERP_WEB_DEMO_PROJECT, ERP_WEB_DEMO_NEW_ISSUE_URL, ERP_WEB_DEMO_FIND_TEST_ISSUE_URL],
    [ERP_SERVER_FIND_ISSUE_URL, ERP_SERVER_PROJECT, ERP_SERVER_NEW_ISSUE_URL, ERP_SERVER_FIND_TEST_ISSUE_URL]
  ]

  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except  Exception as error:
  print("Main, Environment variable does not exist: ",  type(error).__name__, "–", error)

def collect_gitlab_issues(driver, wait, issue_link_list):
  for proj_url in project_links:
    print(proj_url[0])
    print(proj_url[1])
    try:
      driver.get(proj_url[0])
      get_gitlab_issue_info(driver, wait, proj_url[1], proj_url[2], issue_link_list)
    except Exception as error:
      print("Collect Gitlab Issues, Exception: ", type(error).__name__, "–", error)
      slack_protocol.send_survey(user="collect", text=str.format(""":speech_balloon: *Error* on *Collect* Gitlab Issues. :anger:\nPlease check this <{0}|issue>.""", proj_url[0]))

def create_testcase(driver, wait):
  print("RPA create_testcase")
  
  gitlabsignin(driver, SIGN_IN_URL, GITLAB_USERNAME, GITLAB_PASSWORD)
  issue_link_list = []
  issue_obj_list = []

  collect_gitlab_issues(driver, wait, issue_link_list)
  oncreate_testcase_update_issue_update_db(TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, driver, wait, issue_link_list, issue_obj_list)
  
  firebase.save(issue_obj_list) # Save to db

  if len(issue_obj_list) > 0:
    slack_protocol.send_survey(user="AAAA", block=slack_protocol.read_blocks(issue_obj_list, [], is_finishing=False, is_creating=True), text="Selenium result")
  else:
    slack_protocol.send_survey(user="no_success", text=":speech_balloon: No new issue found.")

