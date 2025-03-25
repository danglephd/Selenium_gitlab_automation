from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import pyautogui
from ..db.sqlite import GitLab_Issue_Obj
from ..slack import slack_protocol
from .create_testcase_page import oncreate_test_issue_and_file

def oncreate_testcase_update_issue_update_db(TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, driver, wait, issue_link_list, issue_obj_list):
    print(">>>oncreate_testcase_update_issue_update_db")
    for iss_number_item, issue_url_item, project_item, new_issue_url_item, issue_text_item in issue_link_list:
        # # create test issue
        issue_test_url, path = oncreate_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number_item, project_item, new_issue_url_item, issue_text_item)
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

def remove_label_needtotest(wait, url):
    print(">>> remove_label_needtotest")

    try:
        elem_needtotest = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='Need to test']/button")))
        elem_needtotest.click()
    except TimeoutException as ex:
        print("Remove label needtotest, Exception: " + str(ex.msg))
        slack_protocol.send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *Need_to_test*. :anger:\nPlease check this <{0}|issue>.""", url))

def onfinish_update_label_and_return_Query(driver, wait, issue_url_item, id):
    # print("update_gitlab_issues", issue_url_item, id)
    # update main issue
    driver.get(issue_url_item)
    time.sleep(3)
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
    driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
    elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
    elem_find_label.click()

    elem_find_label.send_keys("Test Pass")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    elem_find_label.send_keys("wf:Ready_for_UAT")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")))
    elem_close_asssign_label = driver.find_element(By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")
    elem_close_asssign_label.click()

    time.sleep(1)
    remove_label_qa(wait, issue_url_item)
    
    # # return query
    return """UPDATE ISSUE
SET test_state = 'Done'
WHERE id = {0};
""".format(id)

def onfinish_add_desc_and_attach_file(driver, wait, test_issue_url, project, test_file_path):
    # print("update_gitlab_test_issues", test_issue_url, project, test_file_path)
    driver.get(test_issue_url)
    driver.set_window_size(1047, 652)
    issue_test_desc = """Test Pass.

Please check the attach file for test result detail.

"""
    driver.find_element(By.ID, "note-body").send_keys(issue_test_desc)
    bt_attach_file = driver.find_element(By.XPATH, "//button[@title='Attach a file or image']")
    bt_attach_file.click() # Attach file
    time.sleep(1)
    pyautogui.write(test_file_path) 
    pyautogui.press('enter')

    time.sleep(3)
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-confirm btn-md gl-button split-content-button']")))
    elem.click()

def remove_label_qa(wait, url):
    try:
        elem_qa = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='wf:QA']/button")))
        elem_qa.click()
    except Exception as ex:
        print("Remove label wf:QA, Exception: " + str(ex.msg))
        slack_protocol.send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *wf:QA*. :anger:\nPlease check this <{0}|issue>.""", url))
