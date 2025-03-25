from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time
from .excel_file_testcase_manage import create_testcase_file, update_file_testcase

def oncreate_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number, project, new_issue_url, issue_text_item):
    print(">>> create_test_issue_and_file")
    issue_test_name = TEST_ISSUE_TEMP + iss_number
    issue_test_desc = TEST_ISSUE_DESC_TEMP + " #" + iss_number
    driver.get(new_issue_url)
    driver.find_element(By.ID, "issue_title").send_keys(issue_test_name)
    driver.find_element(By.ID, "issue_description").send_keys(issue_test_desc)
    a_assign_to_me_link = driver.find_element(By.XPATH, "//a[@data-qa-selector='assign_to_me_link']")
    a_assign_to_me_link.click() # Assign issue test to QA
    driver.find_element(By.XPATH, "//button[@type='submit']").click() # Create test Issue
    
    issue_test_url = driver.current_url
    issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    while not issue_test_number.isnumeric():
        print(">>>>warning: ", issue_test_number)
        time.sleep(0.1)
        issue_test_url = driver.current_url
        issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    file_name = "{0}-{1}-{2}".format(TEST_ISSUE_FILE_TEMP, iss_number, issue_test_number)
    print(">>>>New Test Issue url: ", issue_test_url)
    # Add Test Label>>
    time.sleep(3)
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
    driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
    elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
    elem_find_label.click()

    elem_find_label.send_keys("Test")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)
    # <<
    driver.find_element(By.XPATH, "//button[@data-qa-selector='related_issues_plus_button']").click() # Open textbox to input 
    driver.find_element(By.ID, "add-related-issues-form-input").send_keys(iss_number + " ") # Input related issue 
    driver.find_element(By.XPATH, "//button[@type='submit']").click() # Click Add button
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='related-items-list content-list']"))) # Wait for finish add related 
    folder_name = TEST_ISSUE_FOLDER_TEMP + iss_number
    path = create_testcase_file(iss_number, project, folder_name, file_name)
    update_file_testcase(path, issue_test_number, issue_test_desc, issue_text_item)
    return issue_test_url, path
