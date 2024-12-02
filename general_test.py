import pytest
from rpa_gitlab_qa import TestRPA_GitlabQA
from slack_webhook import *
  
rpa_gitlabQA = TestRPA_GitlabQA()

class TestGeneral():

#  Test case 
  def test_migrate_SQLiteDb(self):
    rpa_gitlabQA.migrate_SQLiteDb()
    
  def test_create_testcase(self):
    rpa_gitlabQA.create_testcase()
    send_survey(user="AAAA", block=self.read_blocks(is_finishing=False, is_creating=True), text="Selenium result")

  def test_finish_testcase(self):
    rpa_gitlabQA.finish_testcase()
    send_survey(user="AAAA", block=self.read_blocks(is_finishing=True, is_creating=False), text="Selenium result")

  def test_migrate_firebase_db(self):
    rpa_gitlabQA.migrate_firebase_db()
