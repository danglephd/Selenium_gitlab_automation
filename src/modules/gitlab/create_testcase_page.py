from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from ..db.sqlite import GitLab_Issue_Obj
from ..slack import send
from .excel_file_testcase_manage import create_testcase_file, update_file_testcase

def create_testcase_update_issue_update_db(TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, driver, wait, issue_link_list):
    issue_obj_list = []
    for iss_number_item, issue_url_item, project_item, new_issue_url_item, issue_text_item in issue_link_list:
        # # create test issue
        issue_test_url, path = create_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number_item, project_item, new_issue_url_item, issue_text_item)
        issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
        
        # update main issue
        driver.get(issue_url_item)
        time.sleep(3)
        elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
        driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
        elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
        elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
        elem_find_label.click()

        elem_find_label.send_keys("Test case")
        elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
        time.sleep(1)
        elem_testcase.send_keys(Keys.SPACE)
        # elem_dropdown = driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
        # elem_dropdown.click()

        # elem_find_label.send_keys("Need to ")
        # elem_needtotest = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
        # time.sleep(3)
        # elem_needtotest.send_keys(Keys.SPACE)
        # # elem_dropdown = driver.find_element(By.XPATH, "//button[@class='dropdown-item is-focused']")
        # # elem_dropdown.click()

        elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@title='Edit title and description']")))
        elem_edit = driver.find_element(By.XPATH, "//button[@title='Edit title and description']")
        elem_edit.click()

        time.sleep(1)
        remove_label_needtotest(wait, url=issue_url_item)

        # # update db
        item = GitLab_Issue_Obj(id=0, project=project_item, path=path, test_state="Created", issue_test_url=issue_test_url, issue_test_number=issue_test_number, issue_number=iss_number_item, issue_url=issue_url_item, duedate=" "
        
        # 0, project_item, path, "Created", issue_test_url, issue_test_number, iss_number_item, issue_url_item
        )
        issue_obj_list.append(item)

def create_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number, project, new_issue_url, issue_text_item):
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

def remove_label_needtotest(wait, url):
    try:
        elem_needtotest = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='Need to test']/button")))
        elem_needtotest.click()
    except TimeoutException as ex:
        print("Remove label needtotest, Exception: " + str(ex.msg))
        send.send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *Need_to_test*. :anger:\nPlease check this <{0}|issue>.""", url))
