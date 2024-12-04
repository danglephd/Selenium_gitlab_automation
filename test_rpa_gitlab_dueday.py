# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
from datetime import datetime

issue_duedate_list = []
date_format = '%b %d, %Y'
 
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
  XM_WEB_V2_FIND_ISSUE_URL = os.environ["XM_WEB_V2_FIND_ISSUE_URL"]
  XM_API_FIND_ISSUE_URL = os.environ["XM_API_FIND_ISSUE_URL"]
  XM_API_V2_FIND_ISSUE_URL = os.environ["XM_API_V2_FIND_ISSUE_URL"]
  XM_LA_FIND_ISSUE_URL = os.environ["XM_LA_FIND_ISSUE_URL"]
  ERP_WEB_FIND_ISSUE_URL = os.environ["ERP_WEB_FIND_ISSUE_URL"]
  ERP_SERVER_FIND_ISSUE_URL = os.environ["ERP_SERVER_FIND_ISSUE_URL"]
  ADMIN_PAGE_FIND_ISSUE_URL = os.environ["ADMIN_PAGE_FIND_ISSUE_URL"]
  ERP_XML_TO_SQL_FIND_ISSUE_URL = os.environ["ERP_XML_TO_SQL_FIND_ISSUE_URL"]
  
  XM_WEB_FIND_TEST_ISSUE_URL = os.environ["XM_WEB_FIND_TEST_ISSUE_URL"]
  XM_WEB_V2_FIND_TEST_ISSUE_URL = os.environ["XM_WEB_V2_FIND_TEST_ISSUE_URL"]
  XM_API_FIND_TEST_ISSUE_URL = os.environ["XM_API_FIND_TEST_ISSUE_URL"]
  XM_API_V2_FIND_TEST_ISSUE_URL = os.environ["XM_API_V2_FIND_TEST_ISSUE_URL"]
  XM_LA_FIND_TEST_ISSUE_URL = os.environ["XM_LA_FIND_TEST_ISSUE_URL"]
  ERP_WEB_FIND_TEST_ISSUE_URL = os.environ["ERP_WEB_FIND_TEST_ISSUE_URL"]
  ERP_SERVER_FIND_TEST_ISSUE_URL = os.environ["ERP_SERVER_FIND_TEST_ISSUE_URL"]
  ADMIN_PAGE_FIND_TEST_ISSUE_URL = os.environ["ADMIN_PAGE_FIND_TEST_ISSUE_URL"]
  ERP_XML_TO_SQL_FIND_TEST_ISSUE_URL = os.environ["ERP_XML_TO_SQL_FIND_TEST_ISSUE_URL"]
  
  XM_WEB_NEW_ISSUE_URL = os.environ["XM_WEB_NEW_ISSUE_URL"]
  XM_WEB_V2_NEW_ISSUE_URL = os.environ["XM_WEB_V2_NEW_ISSUE_URL"]
  XM_API_NEW_ISSUE_URL = os.environ["XM_API_NEW_ISSUE_URL"]
  XM_API_V2_NEW_ISSUE_URL = os.environ["XM_API_V2_NEW_ISSUE_URL"]
  XM_LA_NEW_ISSUE_URL = os.environ["XM_LA_NEW_ISSUE_URL"]
  ERP_WEB_NEW_ISSUE_URL = os.environ["ERP_WEB_NEW_ISSUE_URL"]
  ERP_SERVER_NEW_ISSUE_URL = os.environ["ERP_SERVER_NEW_ISSUE_URL"]
  ADMIN_PAGE_NEW_ISSUE_URL = os.environ["ADMIN_PAGE_NEW_ISSUE_URL"]
  ERP_XML_TO_SQL_NEW_ISSUE_URL = os.environ["ERP_XML_TO_SQL_NEW_ISSUE_URL"]

  XM_WEB_PROJECT = os.environ["XM_WEB_PROJECT"]
  XM_WEB_V2_PROJECT = os.environ["XM_WEB_V2_PROJECT"]
  XM_API_PROJECT = os.environ["XM_API_PROJECT"]
  XM_API_V2_PROJECT = os.environ["XM_API_V2_PROJECT"]
  XM_LA_PROJECT = os.environ["XM_LA_PROJECT"]
  ERP_WEB_PROJECT = os.environ["ERP_WEB_PROJECT"]
  ERP_SERVER_PROJECT = os.environ["ERP_SERVER_PROJECT"]
  ADMIN_PAGE_PROJECT = os.environ["ADMIN_PAGE_PROJECT"]
  ERP_XML_TO_SQL_PROJECT = os.environ["ERP_XML_TO_SQL_PROJECT"]

  XM_WEB_FOUND_QA_URL = os.environ["XM_WEB_FOUND_QA_URL"]
  XM_API_FOUND_QA_URL = os.environ["XM_API_FOUND_QA_URL"]
  ERP_WEB_FOUND_QA_URL = os.environ["ERP_WEB_FOUND_QA_URL"]
  ERP_SERVER_FOUND_QA_URL = os.environ["ERP_SERVER_FOUND_QA_URL"]
  
  project_links = [
    # [XM_WEB_V2_FIND_ISSUE_URL, XM_WEB_V2_PROJECT, XM_WEB_V2_NEW_ISSUE_URL],
    # [XM_API_V2_FIND_ISSUE_URL, XM_API_V2_PROJECT, XM_API_V2_NEW_ISSUE_URL],
    # [XM_LA_FIND_ISSUE_URL, XM_LA_PROJECT, XM_LA_NEW_ISSUE_URL, XM_LA_FIND_TEST_ISSUE_URL]
    # [ERP_XML_TO_SQL_FIND_ISSUE_URL, ERP_XML_TO_SQL_PROJECT, ERP_XML_TO_SQL_NEW_ISSUE_URL],
    # [ADMIN_PAGE_FIND_ISSUE_URL, ADMIN_PAGE_PROJECT, ADMIN_PAGE_NEW_ISSUE_URL],

    [XM_WEB_FIND_ISSUE_URL, XM_WEB_PROJECT, XM_WEB_NEW_ISSUE_URL, XM_WEB_FIND_TEST_ISSUE_URL, XM_WEB_FOUND_QA_URL],
    [XM_API_FIND_ISSUE_URL, XM_API_PROJECT, XM_API_NEW_ISSUE_URL, XM_API_FIND_TEST_ISSUE_URL, XM_API_FOUND_QA_URL],
    [ERP_WEB_FIND_ISSUE_URL, ERP_WEB_PROJECT, ERP_WEB_NEW_ISSUE_URL, ERP_WEB_FIND_TEST_ISSUE_URL, ERP_WEB_FOUND_QA_URL],
    [ERP_SERVER_FIND_ISSUE_URL, ERP_SERVER_PROJECT, ERP_SERVER_NEW_ISSUE_URL, ERP_SERVER_FIND_TEST_ISSUE_URL, ERP_SERVER_FOUND_QA_URL]
  ]

  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except KeyError:
  print("Main, Environment variable does not exist", KeyError)


class TestRPA_Gitlab_Dueday():

  def setup_method(self, method):
    delay = 5 # seconds
    # self.driver = webdriver.Chrome()
    service = Service()
    options = webdriver.ChromeOptions()
    self.driver = webdriver.Chrome(service=service, options=options)
    self.wait = WebDriverWait(self.driver, delay)
    self.vars = {}
    # print("1")
  
  def teardown_method(self, method):
    self.driver.quit()
    # print("3nd")

  def get_gitlab_issue_info_duedate(self):
    print(">Get Gitlab Issue Information with duedate")
    try:
      elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='content-list issuable-list issues-list']/li")))
      # print(">>>>elem: ", elem)
      elems = self.driver.find_elements(By.XPATH, "//div[@class='issuable-list-container']/ul/li")
      # print(">>>>elems: ", elems)
      for li in elems:
        # print('>>>li', li)
        att = li.get_attribute("data-qa-issuable-title")
        # print('>>>att li', att)
        ele_issue_name = li.find_element(By.CLASS_NAME, "issuable-reference")
        issue_no_txt = ele_issue_name.text
        date_obj = issue_duedate_txt = ""
        datetime.min
        try:
          ele_issue_duedate = li.find_element(By.CLASS_NAME, "issuable-due-date")
          issue_duedate_txt = ele_issue_duedate.text
          date_obj = datetime.strptime(issue_duedate_txt, date_format)
        except NoSuchElementException as ex:
            print("Exception: no such element. " + str(ex.msg))
        # print(">>>>issue_no_txt: ", issue_no_txt)
        # print(">>>>issue_duedate_txt: ", issue_duedate_txt)
        # print(">>>>date_obj: ", date_obj)
        iss_number = issue_no_txt[1:]
        issue_duedate_list.append([iss_number, issue_duedate_txt])
      print(">>>>issue_duedate_list: ", issue_duedate_list)
      return 
    except TimeoutException as ex:
      print("Exception has been thrown. " + str(ex.msg))
      # send_survey(user="get", text=""":interrobang::interrobang::interrobang: *Error* on *Get Gitlab Issue Information.* :broken_heart::broken_heart::broken_heart:\nPlease get help from your Administrator.""")

# Finish processes

# <<<<

  def gitlabsignin(self):
    print("gitlabsignin")
    self.driver.get(SIGN_IN_URL)
    self.driver.maximize_window()
    self.driver.find_element(By.ID, "user_login").send_keys(GITLAB_USERNAME)
    self.driver.find_element(By.ID, "user_password").send_keys(GITLAB_PASSWORD)
    submit_ele = self.driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_ele.click()

  def collect_issue_duedate(self):
    print("RPA collect_issue_duedate")
    self.gitlabsignin()
    for proj_url in project_links:
      print(proj_url[0])
      print(proj_url[4])
      try:
        self.driver.get(proj_url[4])
        self.get_gitlab_issue_info_duedate()
      except Exception as ex:
        print("Collect Gitlab Issues Dueday, Exception: " + str(ex.msg))
        send_survey(user="collect", text=str.format(""":speech_balloon: *Error* on *Collect* Gitlab Issues *Duedate*. :anger:\nPlease check this <{0}|issue>.""", proj_url[0]))
    
    if(len(issue_duedate_list) > 0):
      for row in issue_duedate_list:
        query = """UPDATE ISSUE
          SET duedate = '{0}'
          WHERE id = {1};
          """.format(row[1], row[0])
        # print(query)
        sqlite.executeQuery(query) # Save to db
        
    self.driver.close()

# db migrate db

# <<<<<<<<<<<<<<

#  Test case 
  
  def test_collect_duedate(self):
    self.collect_issue_duedate()
    # send_survey(user="AAAA", block=self.read_blocks(is_finishing=False, is_creating=True), text="Selenium result")

# <<<<
