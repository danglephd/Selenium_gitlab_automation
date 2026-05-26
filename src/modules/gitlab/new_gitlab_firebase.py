import os
from .signin_page import gitlabsignin
from .find_issue_page import get_gitlab_issue_info
from .update_testcase_page import oncreate_testcase_update_issue_update_db
from ..db import firebase

from dotenv import load_dotenv
from ..helper import write_log

from ..slack import slack_protocol

try:
  load_dotenv()
  write_log("=== Script Started ===")
  write_log("Loading environment variables...")
  
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
  
  write_log("✓ All environment variables loaded successfully")
  
  project_links = [
    # [XM_WEB_V2_FIND_ISSUE_URL, XM_WEB_V2_PROJECT, XM_WEB_V2_NEW_ISSUE_URL],
    # [XM_API_V2_FIND_ISSUE_URL, XM_API_V2_PROJECT, XM_API_V2_NEW_ISSUE_URL],
    # [ERP_XML_TO_SQL_FIND_ISSUE_URL, ERP_XML_TO_SQL_PROJECT, ERP_XML_TO_SQL_NEW_ISSUE_URL],
    # [ADMIN_PAGE_FIND_ISSUE_URL, ADMIN_PAGE_PROJECT, ADMIN_PAGE_NEW_ISSUE_URL],
    # [ERP_WEB_DEMO_FIND_ISSUE_URL, ERP_WEB_DEMO_PROJECT, ERP_WEB_DEMO_NEW_ISSUE_URL, ERP_WEB_DEMO_FIND_TEST_ISSUE_URL],

    [XM_LA_FIND_ISSUE_URL, XM_LA_PROJECT, XM_LA_NEW_ISSUE_URL, XM_LA_FIND_TEST_ISSUE_URL],
    # [XM_WEB_FIND_ISSUE_URL, XM_WEB_PROJECT, XM_WEB_NEW_ISSUE_URL, XM_WEB_FIND_TEST_ISSUE_URL],
    # [XM_API_FIND_ISSUE_URL, XM_API_PROJECT, XM_API_NEW_ISSUE_URL, XM_API_FIND_TEST_ISSUE_URL],
    # [ERP_WEB_FIND_ISSUE_URL, ERP_WEB_PROJECT, ERP_WEB_NEW_ISSUE_URL, ERP_WEB_FIND_TEST_ISSUE_URL],
    # [ERP_SERVER_FIND_ISSUE_URL, ERP_SERVER_PROJECT, ERP_SERVER_NEW_ISSUE_URL, ERP_SERVER_FIND_TEST_ISSUE_URL]
  ]
  
  write_log(f"Configured {len(project_links)} active project links")

except  Exception as error:
  error_msg = f"Main, Environment variable does not exist: {type(error).__name__} – {error}"
  print(error_msg)
  write_log(f"✗ ERROR: {error_msg}")

def collect_gitlab_issues(driver, wait, issue_link_list):
  write_log("--- Starting collect_gitlab_issues function ---")
  write_log(f"Total projects to process: {len(project_links)}")
  
  processed_count = 0
  for proj_url in project_links:
    processed_count += 1
    write_log(f"\n[Project {processed_count}/{len(project_links)}]")
    write_log(f"Processing URL: {proj_url[0]}")
    write_log(f"Project: {proj_url[1]}")
    
    try:
      write_log("Navigating to project URL...")
      driver.get(proj_url[0])
      write_log("✓ Successfully loaded project page")
      
      write_log("Fetching GitLab issue information...")
      get_gitlab_issue_info(driver, wait, proj_url[1], proj_url[2], issue_link_list)
      write_log(f"✓ Successfully collected issues for project {proj_url[1]}")
      write_log(f"Total issues collected so far: {len(issue_link_list)}")
      
    except Exception as error:
      error_msg = f"Collect Gitlab Issues, Exception: {type(error).__name__} – {error}"
      write_log(f"✗ ERROR: {error_msg}")
      print(error_msg)
      
      try:
        slack_protocol.send_survey(user="collect", text=str.format(""":speech_balloon: *Error* on *Collect* Gitlab Issues. :anger:\nPlease check this <{0}|issue>.""", proj_url[0]))
        write_log("✓ Error notification sent to Slack")
      except Exception as slack_error:
        write_log(f"✗ Failed to send Slack notification: {slack_error}")
  
  write_log(f"--- Finished collect_gitlab_issues function ---")
  write_log(f"Total issues collected: {len(issue_link_list)}")

def create_testcase(driver, wait):
  write_log("\n" + "="*60)
  write_log(">>> STARTING CREATE_TESTCASE WORKFLOW <<<")
  write_log("="*60)
  
  try:
    # Step 1: GitLab Sign In
    write_log("\n[Step 1/4] Logging into GitLab...")
    write_log(f"Sign-in URL: {SIGN_IN_URL}")
    gitlabsignin(driver, SIGN_IN_URL, GITLAB_USERNAME, GITLAB_PASSWORD)
    write_log("✓ Successfully signed into GitLab")
    
    # Step 2: Collect Issues
    issue_link_list = []
    issue_obj_list = []
    
    write_log("\n[Step 2/4] Collecting GitLab issues...")
    collect_gitlab_issues(driver, wait, issue_link_list)
    write_log(f"✓ Completed issue collection. Found {len(issue_link_list)} issues")
    
    # Step 3: Update Issues and Database
    write_log("\n[Step 3/4] Creating test cases and updating issues...")
    write_log(f"Test Case Folder: {TEST_ISSUE_FOLDER_TEMP}")
    write_log(f"Test Issue Template: {TEST_ISSUE_TEMP}")
    
    oncreate_testcase_update_issue_update_db(
        TEST_ISSUE_TEMP, 
        TEST_ISSUE_DESC_TEMP, 
        TEST_ISSUE_FILE_TEMP, 
        TEST_ISSUE_FOLDER_TEMP, 
        driver, 
        wait, 
        issue_link_list, 
        issue_obj_list
    )
    write_log(f"✓ Successfully created {len(issue_obj_list)} test cases")
    
    # Step 4: Save to Firebase
    write_log("\n[Step 4/4] Saving data to Firebase database...")
    firebase.save(issue_obj_list)
    write_log(f"✓ Successfully saved {len(issue_obj_list)} records to Firebase")
    
    # Step 5: Send Slack Notification
    write_log("\n[Step 5/4] Sending Slack notification...")
    if len(issue_obj_list) > 0:
      write_log(f"Sending success notification with {len(issue_obj_list)} records to Slack...")
      slack_protocol.send_survey(
          user="AAAA", 
          block=slack_protocol.read_blocks(issue_obj_list, [], is_finishing=False, is_creating=True), 
          text="Selenium result"
      )
      write_log("✓ Slack notification sent successfully")
    else:
      write_log("⚠ No new issues found - sending info notification to Slack...")
      slack_protocol.send_survey(user="no_success", text=":speech_balloon: No new issue found.")
      write_log("✓ Info notification sent to Slack")
    
    write_log("\n" + "="*60)
    write_log(">>> CREATE_TESTCASE WORKFLOW COMPLETED SUCCESSFULLY <<<")
    write_log("="*60)
    
  except Exception as error:
    error_msg = f"CRITICAL ERROR in create_testcase: {type(error).__name__} – {error}"
    write_log(f"\n✗ {error_msg}")
    print(error_msg)
    write_log("\n" + "="*60)
    write_log(">>> CREATE_TESTCASE WORKFLOW FAILED <<<")
    write_log("="*60)
    raise

