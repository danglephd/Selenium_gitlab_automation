import pytest
from src.modules.gitlab import new_gitlab_firebase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

class TestRPA_Create_Testcase_FB:

    def setup_method(self, method):
        delay = 5 # seconds
# self.driver = webdriver.Chrome()
        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Chạy trình duyệt ở chế độ headless
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, delay)
        self.vars = {}
        print("Setup completed")

    def teardown_method(self, method):
        self.driver.quit()
        print("Teardown completed")

    def test_create_testcase(self):
        try:
            new_gitlab_firebase.create_testcase(self.driver, self.wait)
            # Thêm kiểm tra kết quả (assertions)
            assert "expected_result" in self.driver.page_source, "Test case creation failed"
        except TimeoutException as e:
            pytest.fail(f"Timeout occurred: {e}")
        finally:
            self.driver.quit()
