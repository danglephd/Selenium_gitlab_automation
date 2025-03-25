import pytest
from src.modules.gitlab import create_gitlab
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException

class TestRPA_Create_Testcase():

    def setup_method(self, method):
        delay = 5 # seconds
        # self.driver = webdriver.Chrome()
        service = Service()
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, delay)
        self.vars = {}
        print("1")
    
    def teardown_method(self, method):
        self.driver.quit()
        print("3nd")

    def test_create_testcase(self):
        create_gitlab.create_testcase(self.driver, self.wait)
        self.driver.close()
