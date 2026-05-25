from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time
from .excel_file_testcase_manage import create_testcase_file, update_file_testcase
from ..helper import write_log

def oncreate_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number, project, new_issue_url, issue_text_item):
    write_log(f">>> create_test_issue_and_file for Issue #{iss_number}")
    write_log(f"Project: {project}")
    write_log(f"New Issue URL: {new_issue_url}")

    issue_test_name = TEST_ISSUE_TEMP + iss_number
    issue_test_desc = TEST_ISSUE_DESC_TEMP + " #" + iss_number
    
    write_log(f"Test Issue Name: {issue_test_name}")
    write_log(f"Test Issue Description: {issue_test_desc}")

    driver.get(new_issue_url)
    
    write_log(f"[2/6] Filling issue title: {issue_test_name}")

    # add wait for input appear
    wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='work-item-title-input']")))

    driver.find_element(By.CSS_SELECTOR, "input[data-testid='work-item-title-input']").send_keys(issue_test_name)
    
    write_log(f"[3/6] Filling issue description")
    
    driver.find_element(By.CSS_SELECTOR, "textarea[data-testid='markdown-editor-form-field']").send_keys(issue_test_desc)
    
    # write_log(f"[4/6] Assigning issue to me")
    # a_assign_to_me_link = driver.find_element(By.XPATH, "//a[@data-qa-selector='assign_to_me_link']")
    # a_assign_to_me_link.click() # Assign issue test to QA
    
    write_log(f"[5/6] Creating test issue")
    
    driver.find_element(By.XPATH, "//button[@type='submit']").click() # Create test Issue
    
    issue_test_url = driver.current_url
    issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    while not issue_test_number.isnumeric():
        write_log(f"       Waiting for page redirect (issue number: {issue_test_number})")
        time.sleep(0.1)
        issue_test_url = driver.current_url
        issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
    
    file_name = "{0}-{1}-{2}".format(TEST_ISSUE_FILE_TEMP, iss_number, issue_test_number)
    
    write_log(f"       ✓ Test issue created: {issue_test_url}")
    write_log(f"       [6/6] Adding labels and related issues")
    
    time.sleep(3)
    try:
        # Add Test Label>>
        driver.find_element(
            By.XPATH,
            "//section[@data-testid='work-item-labels']//button[@data-testid='edit-button']"
        ).click()
        elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search']")))
        elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
        elem_find_label.click()

        elem_find_label.send_keys("type:Test")
        # elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
        time.sleep(1)
        elem_find_label.send_keys(Keys.ENTER)
        
        write_log(f"       ✓ 'type:Test' label added")
        write_log(f"       Adding related issue #{iss_number}")
    
        # <<
        driver.find_element(By.XPATH, "//button[@data-testid='link-item-add-button']").click() # Open textbox to input 
        input_el = driver.find_element(
            By.CSS_SELECTOR,
            "input[role='combobox']"
        )

        input_el.send_keys(iss_number + " ")# Input issue number to link
        driver.find_element(By.XPATH, "//button[@data-testid='link-work-item-button']").click() # Click Add button
        elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='work-items-list content-list sortable-container gl-cursor-grab']"))) # Wait for finish add related 
        
        write_log(f"       ✓ Related issue added")
        write_log(f"       Creating test case file")
    
    except Exception as elem_error:
        write_log(f"    ✗ Error processing issue element {type(elem_error).__name__} – {elem_error}")
    folder_name = TEST_ISSUE_FOLDER_TEMP + iss_number
    path = create_testcase_file(iss_number, project, folder_name, file_name)
    
    write_log(f"       Updating file testcase\n")
    
    update_file_testcase(path, issue_test_number, issue_test_desc, issue_text_item)
    
    write_log(f"       ✓ File testcase updated")
    write_log(f"     <<< Completed create_test_issue_and_file\n")
    
    return issue_test_url, path
