import os

import pytest
from dotenv import load_dotenv
from src.modules.gitlab import finish_issue_gitlab_firebase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from src.modules.helper import write_finish_issue_log

load_dotenv()


class TestRPA_Finish_Testcase_FB:

    def setup_method(self, method):
        delay = 5 # seconds
# self.driver = webdriver.Chrome()
        service = Service()
        options = webdriver.ChromeOptions()

        use_headless = os.getenv("HEADLESS", "1").strip().lower() not in {"0", "false", "no", "off"}
        if use_headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-gpu")
        options.add_argument('--log-level=3')  # INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, delay)
        self.vars = {}
        with open("finish-issue.log", "w", encoding="utf-8") as f:
            f.write("Setup completed\n")


    def teardown_method(self, method):
        self.driver.quit()
        write_finish_issue_log("Teardown completed")

    def test_finish_testcase(self):
        try:
            finish_issue_gitlab_firebase.finish_testcase(self.driver, self.wait)
        except TimeoutException as e:
            pytest.fail(f"Timeout occurred: {e}")
        finally:
            write_finish_issue_log("Finalizing test...")
            self.driver.quit()
