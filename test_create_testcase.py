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

project_links = [
                 ["https://git.iptp.net/xm/xm-web/-/issues/?label_name%5B%5D=Need%20to%20test", 'xm-web', "https://git.iptp.net/xm/xm-web/-/issues/new"],
                 ["https://git.iptp.net/andre/xm-api/-/issues/?label_name%5B%5D=Need%20to%20test", "xm-api", "https://git.iptp.net/andre/xm-api/-/issues/new"],
                 ["https://git.iptp.net/erp/erp-web/-/issues/?label_name%5B%5D=Need%20to%20test", "erp-web", "https://git.iptp.net/erp/erp-web/-/issues/new"],
                 ["https://git.iptp.net/erp/erp-server/-/issues/?label_name%5B%5D=Need%20to%20test", "erp-server", "https://git.iptp.net/erp/erp-server/-/issues/new"]
                ]
sign_in_url = "https://git.iptp.net/users/sign_in"
issue_obj_list = []
issue_link_list = []

try:
  load_dotenv()
  GITLAB_USERNAME = os.environ["GITLAB_USERNAME"]
  GITLAB_PASSWORD = os.environ["GITLAB_PASSWORD"]
  TEST_ISSUE_TEMP = os.environ["TEST_ISSUE_TEMP"]
  TEST_ISSUE_FOLDER_TEMP = os.environ["TEST_ISSUE_FOLDER_TEMP"]
  TEST_ISSUE_DESC_TEMP = os.environ["TEST_ISSUE_DESC_TEMP"]
  TEST_ISSUE_FILE_TEMP = os.environ["TEST_ISSUE_FILE_TEMP"]
  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except KeyError:
  print("Environment variable does not exist", KeyError)


class TestGitlab():
  def setup_method(self, method):
    delay = 5 # seconds
    self.driver = webdriver.Chrome()
    self.wait = WebDriverWait(self.driver, delay)
    self.vars = {}
    print("1")
  
  def teardown_method(self, method):
    self.driver.quit()
    print("3nd")
  
  def update_result(self, iss_number):
    self.driver.get("https://docs.google.com/spreadsheets/d/1IATFgzFi9-t5bwlzXBL0l8HdWvyGIkLK/edit?usp=sharing&ouid=111105249960062423142&rtpof=true&sd=true")

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


  def create_test_issue_and_file(self, iss_number, project, new_issue_url):
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
    self.update_file_testcase(path, issue_test_number, issue_test_desc, "")
    return issue_test_url, path

  def get_gitlab_issue_info(self, project, new_issue_url):
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
          # issue_text = tag_a.get_attribute("text")
          print(">>>>url: ", issue_url)
          # print(">>>>text: ", issue_text)
          iss_number = issue_url[issue_url.rfind("/") + 1:]
          print(">>>>iss Number: ", iss_number)
          issue_link_list.append([iss_number, issue_url])
        break # stop run over the li tags
      
      for iss_number_item, issue_url_item in issue_link_list:
        # # create test issue
        issue_test_url, path = self.create_test_issue_and_file(iss_number_item, project, new_issue_url)
        issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
        
        # update main issue
        self.driver.get(issue_url_item)
        elem = self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
        self.driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
        elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
        elem_find_label = self.driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
        elem_find_label.click()

        elem_find_label.send_keys("Test case")
        elem_testcase = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
        time.sleep(3)
        elem_testcase.send_keys(Keys.SPACE)
        # elem_dropdown = self.driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
        # elem_dropdown.click()

        elem_find_label.send_keys("Need to ")
        elem_needtotest = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
        time.sleep(3)
        elem_needtotest.send_keys(Keys.SPACE)
        # elem_dropdown = self.driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
        # elem_dropdown.click()

        elem = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@title='Edit title and description']")))
        elem_edit = self.driver.find_element(By.XPATH, "//button[@title='Edit title and description']")
        elem_edit.click()

        # # update db
        item = GitLab_Issue_Obj(0, project, "Created", path, issue_test_url, issue_test_number, iss_number, issue_url)
        issue_obj_list.append(item)
    except TimeoutException as ex:
      print("Exception has been thrown. " + str(ex.msg))

  def collect_gitlab_issues(self):
    for proj_url in project_links:
      print(proj_url[0])
      print(proj_url[1])
      self.driver.get(proj_url[0])
      self.get_gitlab_issue_info(proj_url[1], proj_url[2])

  def gitlabsignin(self):
    print("gitlabsignin")
    self.driver.get(sign_in_url)
    self.driver.set_window_size(1047, 652)
    self.driver.find_element(By.ID, "user_login").send_keys(GITLAB_USERNAME)
    self.driver.find_element(By.ID, "user_password").send_keys(GITLAB_PASSWORD)
    submit_ele = self.driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_ele.click()

  def test_create_testcase(self):
    print("2")
    self.gitlabsignin()
    self.collect_gitlab_issues()
    sqlite.save(issue_obj_list) # Save to db
    self.driver.close()

  # def test_create_db(self):
  #   print("test_create_db")
  #   playlist = []
  #   sqlite.initTable(playlist)