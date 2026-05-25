from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
from .excel_file_testcase_manage import create_testcase_file, update_file_testcase

def oncreate_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number, project, new_issue_url, issue_text_item):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]     >>> create_test_issue_and_file for Issue #{iss_number}\n")
        f.write(f"[{timestamp}]     Project: {project}\n")
        f.write(f"[{timestamp}]     New Issue URL: {new_issue_url}\n")
    
    issue_test_name = TEST_ISSUE_TEMP + iss_number
    issue_test_desc = TEST_ISSUE_DESC_TEMP + " #" + iss_number
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       [1/6] Navigating to new issue page\n")
    
    driver.get(new_issue_url)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       [2/6] Filling issue title: {issue_test_name}\n")

    # add wait for input appear
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='work-item-title-input']")))

    driver.find_element(By.CSS_SELECTOR, "input[data-testid='work-item-title-input']").send_keys(issue_test_name)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       [3/6] Filling issue description\n")
    
    driver.find_element(By.ID, "work-item-description").send_keys(issue_test_desc)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       [4/6] Assigning issue to me\n")
    
    # a_assign_to_me_link = driver.find_element(By.XPATH, "//a[@data-qa-selector='assign_to_me_link']")
    # a_assign_to_me_link.click() # Assign issue test to QA
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       [5/6] Creating test issue\n")
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click() # Create test Issue
    
    issue_test_url = driver.current_url
    issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    while not issue_test_number.isnumeric():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("collect-issue.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}]       Waiting for page redirect (issue number: {issue_test_number})\n")
        time.sleep(0.1)
        issue_test_url = driver.current_url
        issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    
    file_name = "{0}-{1}-{2}".format(TEST_ISSUE_FILE_TEMP, iss_number, issue_test_number)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       ✓ Test issue created: {issue_test_url}\n")
        f.write(f"[{timestamp}]       [6/6] Adding labels and related issues\n")
    
    # Add Test Label>>
    time.sleep(3)
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
    driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
    elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
    elem_find_label.click()

    elem_find_label.send_keys("type:Test")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       ✓ 'type:Test' label added\n")
        f.write(f"[{timestamp}]       Adding related issue #{iss_number}\n")
    
    # <<
    driver.find_element(By.XPATH, "//button[@data-qa-selector='related_issues_plus_button']").click() # Open textbox to input 
    driver.find_element(By.ID, "add-related-issues-form-input").send_keys(iss_number + " ") # Input related issue 
    driver.find_element(By.XPATH, "//button[@type='submit']").click() # Click Add button
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='related-items-list content-list']"))) # Wait for finish add related 
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       ✓ Related issue added\n")
        f.write(f"[{timestamp}]       Creating test case file\n")
    
    folder_name = TEST_ISSUE_FOLDER_TEMP + iss_number
    path = create_testcase_file(iss_number, project, folder_name, file_name)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       Updating file testcase\n")
    
    update_file_testcase(path, issue_test_number, issue_test_desc, issue_text_item)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("collect-issue.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]       ✓ File testcase updated\n")
        f.write(f"[{timestamp}]     <<< Completed create_test_issue_and_file\n")
    
    return issue_test_url, path
