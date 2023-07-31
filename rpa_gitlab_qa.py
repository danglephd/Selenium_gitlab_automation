# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv
import shutil
import sqlite
from sqlite import GitLab_Issue_Obj
from openpyxl import load_workbook
import pyautogui
from slack_webhook import *
import firebase_db
from enum import Enum

# sign_in_url = "https://git.iptp.net/users/sign_in"
issue_obj_list = []
issue_link_list = []
issue_finished_list = []
 
class DBMSType(Enum):
    SQLITE = 1
    REALTIME = 2

db_selection = DBMSType.SQLITE

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
  XM_API_FIND_ISSUE_URL = os.environ["XM_API_FIND_ISSUE_URL"]
  ERP_WEB_FIND_ISSUE_URL = os.environ["ERP_WEB_FIND_ISSUE_URL"]
  ERP_SERVER_FIND_ISSUE_URL = os.environ["ERP_SERVER_FIND_ISSUE_URL"]
  ADMIN_PAGE_FIND_ISSUE_URL = os.environ["ADMIN_PAGE_FIND_ISSUE_URL"]
  
  XM_WEB_NEW_ISSUE_URL = os.environ["XM_WEB_NEW_ISSUE_URL"]
  XM_API_NEW_ISSUE_URL = os.environ["XM_API_NEW_ISSUE_URL"]
  ERP_WEB_NEW_ISSUE_URL = os.environ["ERP_WEB_NEW_ISSUE_URL"]
  ERP_SERVER_NEW_ISSUE_URL = os.environ["ERP_SERVER_NEW_ISSUE_URL"]
  ADMIN_PAGE_NEW_ISSUE_URL = os.environ["ADMIN_PAGE_NEW_ISSUE_URL"]

  XM_WEB_PROJECT = os.environ["XM_WEB_PROJECT"]
  XM_API_PROJECT = os.environ["XM_API_PROJECT"]
  ERP_WEB_PROJECT = os.environ["ERP_WEB_PROJECT"]
  ERP_SERVER_PROJECT = os.environ["ERP_SERVER_PROJECT"]
  ADMIN_PAGE_PROJECT = os.environ["ADMIN_PAGE_PROJECT"]

  project_links = [
    [XM_WEB_FIND_ISSUE_URL, XM_WEB_PROJECT, XM_WEB_NEW_ISSUE_URL],
    [XM_API_FIND_ISSUE_URL, XM_API_PROJECT, XM_API_NEW_ISSUE_URL],
    [ERP_WEB_FIND_ISSUE_URL, ERP_WEB_PROJECT, ERP_WEB_NEW_ISSUE_URL],
    [ERP_SERVER_FIND_ISSUE_URL, ERP_SERVER_PROJECT, ERP_SERVER_NEW_ISSUE_URL],
    [ADMIN_PAGE_FIND_ISSUE_URL, ADMIN_PAGE_PROJECT, ADMIN_PAGE_NEW_ISSUE_URL]
  ]

  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except KeyError:
  print("Main, Environment variable does not exist", KeyError)


class TestRPA_GitlabQA():
  def setup_method(self, method):
    delay = 5 # seconds
    self.driver = webdriver.Chrome()
    self.wait = WebDriverWait(self.driver, delay)
    self.vars = {}
    print("1")
  
  def teardown_method(self, method):
    self.driver.quit()
    print("3nd")

  def create_testcase_file(self, iss_number, project, folder_name, file_name):
    print("create_testcase_file", iss_number, project, folder_name, file_name)
    path_dst_file_tmp = "D:\\Testcase\\RPA\\{0}\\{1}\\{2}.xlsx"
    path_dst_folder_tmp = "D:\\Testcase\\RPA\\{0}\\{1}"
    path_src = ".\\TEMPLATE\\Testcase-template-{0}.xlsx"
    src = str(path_src.format(project)), 
    path_file_dst = str(path_dst_file_tmp.format(project, folder_name, "".join(file_name)))
    path_folder_dst = str(path_dst_folder_tmp.format(project, folder_name))
    print(src[0], path_file_dst)

    if os.path.exists(path_folder_dst):
      print("Folder is exist: ", path_folder_dst)
    else:
      print("Folder is not exist!", path_folder_dst)
      os.makedirs(path_folder_dst)
    shutil.copy(src[0], path_file_dst)
    
    return path_file_dst

  def update_file_testcase(self, path, iss_test_number, issue_desc, test_scenario):
    print("Update file testcase", path)
    
    #load excel file
    workbook = load_workbook(filename=path)
    
    #open workbook
    sheet = workbook.active
    
    #modify the desired cell
    sheet["C1"] = iss_test_number
    sheet["F1"] = issue_desc
    sheet["B14"] = test_scenario
    
    #save the file
    workbook.save(path)

  def create_test_issue_and_file(self, iss_number, project, new_issue_url, issue_text_item):
    issue_test_name = TEST_ISSUE_TEMP + iss_number
    issue_test_desc = TEST_ISSUE_DESC_TEMP + " #" + iss_number
    self.driver.get(new_issue_url)
    self.driver.find_element(By.ID, "issue_title").send_keys(issue_test_name)
    self.driver.find_element(By.ID, "issue_description").send_keys(issue_test_desc)
    a_assign_to_me_link = self.driver.find_element(By.XPATH, "//a[@data-qa-selector='assign_to_me_link']")
    a_assign_to_me_link.click() # Assign issue test to QA
    self.driver.find_element(By.XPATH, "//button[@type='submit']").click() # Create test Issue
    issue_test_url = self.driver.current_url
    issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    file_name = "{0}-{1}-{2}".format(TEST_ISSUE_FILE_TEMP, iss_number, issue_test_number)
    print(">>>>New Test Issue url: ", issue_test_url)
    self.driver.find_element(By.XPATH, "//button[@data-qa-selector='related_issues_plus_button']").click() # Open textbox to input 
    self.driver.find_element(By.ID, "add-related-issues-form-input").send_keys(iss_number + " ") # Input related issue 
    self.driver.find_element(By.XPATH, "//button[@type='submit']").click() # Click Add button
    elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='related-items-list content-list']"))) # Wait for finish add related 
    folder_name = TEST_ISSUE_FOLDER_TEMP + iss_number
    path = self.create_testcase_file(iss_number, project, folder_name, file_name)
    self.update_file_testcase(path, issue_test_number, issue_test_desc, issue_text_item)
    return issue_test_url, path

  def get_gitlab_issue_info(self, project, new_issue_url):
    print(">Get Gitlab Issue Information")
    try:
      elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='content-list issuable-list issues-list']/li")))
      # print(">>>>elem: ", elem)
      elems = self.driver.find_elements(By.XPATH, "//div[@class='issuable-list-container']/ul/li")
      print(">>>>elems: ", elems)
      for li in elems:
        print('>>>li', li)
        att = li.get_attribute("data-qa-issuable-title")
        print('>>>att li', att)
        tag_a_s = li.find_elements(By.XPATH, "//a[@class='gl-link issue-title-text']")
        # tag_a = x.find_elements_by_tag_name('a')
        for tag_a in tag_a_s:
          print(">>>>tag_a: ", tag_a)
          issue_url = tag_a.get_attribute("href")
          issue_text = tag_a.get_attribute("text")
          print(">>>>url: ", issue_url)
          print(">>>>text: ", issue_text)
          iss_number = issue_url[issue_url.rfind("/") + 1:]
          print(">>>>iss Number: ", iss_number)
          issue_link_list.append([iss_number, issue_url, project, new_issue_url, issue_text])
        break # stop run over the li tags
      # print(">>>>issue_link_list: ", issue_link_list)
      return 
    except TimeoutException as ex:
      print("Exception has been thrown. " + str(ex.msg))
      # send_survey(user="get", text=""":interrobang::interrobang::interrobang: *Error* on *Get Gitlab Issue Information.* :broken_heart::broken_heart::broken_heart:\nPlease get help from your Administrator.""")

  def remove_label_needtotest(self, url):
    try:
      elem_needtotest = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='Need to test']/button")))
      elem_needtotest.click()
    except TimeoutException as ex:
      print("Remove label needtotest, Exception: " + str(ex.msg))
      send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *Need_to_test*. :anger:\nPlease check this <{0}|issue>.""", url))

  def create_testcase_update_issue_update_db(self):
    for iss_number_item, issue_url_item, project_item, new_issue_url_item, issue_text_item in issue_link_list:
      # # create test issue
      issue_test_url, path = self.create_test_issue_and_file(iss_number_item, project_item, new_issue_url_item, issue_text_item)
      issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
      
      # update main issue
      self.driver.get(issue_url_item)
      time.sleep(3)
      elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
      self.driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
      elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
      elem_find_label = self.driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
      elem_find_label.click()

      elem_find_label.send_keys("Test case")
      elem_testcase = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
      time.sleep(1)
      elem_testcase.send_keys(Keys.SPACE)
      # elem_dropdown = self.driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
      # elem_dropdown.click()

      # elem_find_label.send_keys("Need to ")
      # elem_needtotest = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
      # time.sleep(3)
      # elem_needtotest.send_keys(Keys.SPACE)
      # # elem_dropdown = self.driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
      # # elem_dropdown.click()

      elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@title='Edit title and description']")))
      elem_edit = self.driver.find_element(By.XPATH, "//button[@title='Edit title and description']")
      elem_edit.click()

      time.sleep(1)
      self.remove_label_needtotest(url=issue_url_item)

      # # update db
      item = GitLab_Issue_Obj(id=0, project=project_item, path=path, test_state="Created", issue_test_url=issue_test_url, issue_test_number=issue_test_number, issue_number=iss_number_item, issue_url=issue_url_item
        
        # 0, project_item, path, "Created", issue_test_url, issue_test_number, iss_number_item, issue_url_item
        )
      issue_obj_list.append(item)
  
  def collect_gitlab_issues(self):
    for proj_url in project_links:
      print(proj_url[0])
      print(proj_url[1])
      self.driver.get(proj_url[0])
      self.get_gitlab_issue_info(proj_url[1], proj_url[2])

# Finish processes

  def remove_label_qa(self, url):
    try:
      elem_qa = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='wf:QA']/button")))
      elem_qa.click()
    except Exception as ex:
      print("Remove label wf:QA, Exception: " + str(ex.msg))
      send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *wf:QA*. :anger:\nPlease check this <{0}|issue>.""", url))

  def collect_finish_gitlab_issues(self):
    
    match db_selection:
      case DBMSType.SQLITE:
        # SQLitedb
        criteria = "WHERE test_state LIKE 'Finish'"
        issue_list = sqlite.getListIssue(criteria)
      case DBMSType.REALTIME:
        # Firebasedb
        criteria = ['test_state', 'Finish']
        issue_list = firebase_db.getListIssue(criteria)

    if len(issue_list) > 0:
      for item in issue_list:
        issue_finished_list.append(item)

  def update_gitlab_test_issues(self, test_issue_url, project, test_file_path):
    # print("update_gitlab_test_issues", test_issue_url, project, test_file_path)
    self.driver.get(test_issue_url)
    self.driver.set_window_size(1047, 652)
    issue_test_desc = """Test Pass.

Please check the attach file for test result detail.

"""
    self.driver.find_element(By.ID, "note-body").send_keys(issue_test_desc)
    bt_attach_file = self.driver.find_element(By.XPATH, "//button[@title='Attach a file or image']")
    bt_attach_file.click() # Attach file
    time.sleep(1)
    pyautogui.write(test_file_path) 
    pyautogui.press('enter')

    time.sleep(3)
    elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-confirm btn-md gl-button split-content-button']")))
    elem.click()

  def update_gitlab_issues(self, issue_url_item, id):
    # print("update_gitlab_issues", issue_url_item, id)
    # update main issue
    self.driver.get(issue_url_item)
    time.sleep(3)
    elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
    self.driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
    elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
    elem_find_label = self.driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
    elem_find_label.click()

    elem_find_label.send_keys("Test Pass")
    elem_testcase = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    elem_find_label.send_keys("wf:Ready_for_UAT")
    elem_testcase = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")))
    elem_close_asssign_label = self.driver.find_element(By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")
    elem_close_asssign_label.click()

    time.sleep(1)
    self.remove_label_qa(issue_url_item)
    
    # # return query
    return """UPDATE ISSUE
SET test_state = 'Done'
WHERE id = {0};
""".format(id)
  
# <<<<

  def gitlabsignin(self):
    print("gitlabsignin")
    self.driver.get(SIGN_IN_URL)
    self.driver.maximize_window()
    self.driver.find_element(By.ID, "user_login").send_keys(GITLAB_USERNAME)
    self.driver.find_element(By.ID, "user_password").send_keys(GITLAB_PASSWORD)
    submit_ele = self.driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_ele.click()

  def create_testcase(self):
    print("RPA create_testcase")
    self.gitlabsignin()
    self.collect_gitlab_issues()
    self.create_testcase_update_issue_update_db()
    
    match db_selection:
      case DBMSType.SQLITE:
        #Save to SQLiteDB
        sqlite.save(issue_obj_list) # Save to db
      case DBMSType.REALTIME:
        #Save to firebaseDB
        firebase_db.save(issue_obj_list) # Save to db
    self.driver.close()

  def finish_testcase(self):
    print("RPA finish_testcase")
    self.collect_finish_gitlab_issues()
    # query_lst = []
    if(len(issue_finished_list) > 0):
      self.gitlabsignin()
      for row in issue_finished_list:
        # id, project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url
        self.update_gitlab_test_issues(test_issue_url=row.issue_test_url, project=row.project, test_file_path=row.path)
        # query_lst.append(self.update_gitlab_issues(issue_url_item=row.issue_url, id=row.id))
        query = self.update_gitlab_issues(issue_url_item=row.issue_url, id=row.id)

        match db_selection:
          case DBMSType.SQLITE:
            # Update SQLiteDb
            sqlite.executeQuery(query) # Save to db
          case DBMSType.REALTIME:
            # Update FirebaseDb
            firebase_db.update_testcase_status(issue_url=row.issue_url)
    self.driver.close()

  def read_blocks(self, is_finishing=False, is_creating=False):
    issue_summary = "*Collected {0} issue(s):*\n{1}"
    finish_summary = "*Finish {0} issue(s):*\n{1}"

    issue_summary = issue_summary.format(len(issue_obj_list), self.get_list_issue(issue_obj_list))
    finish_summary = finish_summary.format(len(issue_finished_list), self.get_list_issue(issue_finished_list))
    data = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":mega: RPA Process completed success. :rocket::rocket:"
            }
        }
    ]

    if is_finishing:
      data.append(
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": finish_summary
                }
            ]
        }
      )
      
    if is_creating:
      data.append(
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": issue_summary
                }
            ]
        }
      )
    return data

  def get_list_issue(self, issue_arr):
    txt = ""
    for issue in issue_arr:
        txt = txt + str.format("<{0}|{1}>, ", issue.issue_url,  issue.issue_number)
    return txt


# db migrate db
  def migrate_firebase_db(self):
    print('>>>migrate_firebase_db')
    criteria = ""
    issue_list = sqlite.getListIssue(criteria)
    print('>>>len', len(issue_list))
    save_item = []
    for issue_item in issue_list:
      criteria = ['issue_url', issue_item.issue_url]
      data = firebase_db.getListIssue(criteria)
      if len(data) <= 0:
        save_item.append(issue_item)
      else:
        print('>>>Exist item, ', len(data))
        item_to_update = None
        for item in data:
          if item.issue_test_url == issue_item.issue_test_url:
            item_to_update = item
            break
        if item_to_update is None:
          save_item.append(issue_item)
        else:
          firebase_db.update(item_to_update)

    if len(save_item) > 0:
      print('>>>Save len: ',  len(save_item) )
      firebase_db.save(save_item) 

  def migrate_SQLiteDb(self):
    print('>>>migrate_SQLiteDb')
    issue_list = firebase_db.getAllIssue()
    print('>>>len', len(issue_list))

    for issue_item in issue_list:
      criteria = "WHERE issue_url = '{0}' and issue_test_url = '{1}'"
      data = sqlite.getListIssue(str.format(criteria, issue_item.issue_url, issue_item.issue_test_url))
      if len(data) <= 0:
        sqlite.save([issue_item]) 
      else:
        print('>>>Exist item, ', len(data))
        for item in data:
          query = """UPDATE ISSUE
SET test_state = '{1}'
WHERE id = {0} and test_state = 'Create';
""".format(item.id, issue_item.test_state)
          sqlite.executeQuery(query) 


  def create_firebase_db(self):
    firebase_db.create_db()

# <<<<<<<<<<<<<<

#  Test case 
  
  # def test_migrate_SQLiteDb(self):
  #   self.migrate_SQLiteDb()

  def test_create_testcase(self):
    self.create_testcase()
    send_survey(user="AAAA", block=self.read_blocks(is_finishing=False, is_creating=True), text="Selenium result")

  def test_finish_testcase(self):
    self.finish_testcase()
    send_survey(user="AAAA", block=self.read_blocks(is_finishing=True, is_creating=False), text="Selenium result")

  # def test_notification(self):
  #   send_survey(user="AAAA", block=self.read_blocks(), text="Hello hhskdfjhfk")
    
  def test_migrate_firebase_db(self):
    self.migrate_firebase_db()

  # def test_create_firebase_db(self):
  #   self.create_firebase_db()


# <<<<
