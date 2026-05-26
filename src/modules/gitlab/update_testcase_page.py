from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import pyautogui
from ..db.sqlite import GitLab_Issue_Obj
from ..slack import slack_protocol
from .create_testcase_page import oncreate_test_issue_and_file
from ..helper import write_log

def oncreate_testcase_update_issue_update_db(TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, driver, wait, issue_link_list, issue_obj_list):
    write_log(f">>> Starting oncreate_testcase_update_issue_update_db with {len(issue_link_list)} issues to process")
    label_name = "Test case"
    label_need_to_test = "Need to test"

    for iss_number_item, issue_url_item, project_item, new_issue_url_item, issue_text_item in issue_link_list:
        write_log(f"Processing Issue #{iss_number_item}")
        try:
            # # create test issue
            write_log(f"[Step 1] Creating test issue and file for Issue #{iss_number_item}")
            
            issue_test_url, path = oncreate_test_issue_and_file(driver, wait, TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP, TEST_ISSUE_FILE_TEMP, TEST_ISSUE_FOLDER_TEMP, iss_number_item, project_item, new_issue_url_item, issue_text_item)
            issue_test_number = issue_test_url[issue_test_url.rfind("/") + 1:]
            
            write_log(f"       ✓ Test issue created: #{issue_test_number}")
            write_log(f"       [Step 2] Updating main issue")
            
            # update main issue
            driver.get(issue_url_item)
            time.sleep(3)
            
            write_log(f"       Opening edit panel")
            
            driver.find_element(
                By.XPATH,
                "//section[@data-testid='work-item-labels']//button[@data-testid='edit-button']"
            ).click()
            elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search']")))
            elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
            elem_find_label.click()

            write_log(f"       Adding 'Test case' label")

            # Add 'type:Test' label
            elem_find_label.send_keys(label_name)
            # elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
            label_item = wait.until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//li[@role='option'][contains(., '{label_name}')]"
                    )
                )
            )
            label_item.click()  # Click to add label

            time.sleep(1)
            # elem_find_label.send_keys(Keys.ENTER)

            write_log(f"       ✓ 'Test case' label added")
            write_log(f"       Removing 'Need to test' label")

            # Remove label 'Need to test'
            elem_find_label.send_keys(label_need_to_test)
            # elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
            label_need_to_test_item = wait.until(
                expected_conditions.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//li[@role='option'][contains(., '{label_need_to_test}')]"
                    )
                )
            )
            label_need_to_test_item.click()  # Click to add label
            time.sleep(1)
            # elem_find_label.send_keys(Keys.ENTER)

            write_log(f"       ✓ 'Need to test' label removed")
            write_log(f"       Closing edit panel")

            btn_edit = driver.find_element(
                By.CSS_SELECTOR,
                "button[data-testid='work-item-edit-form-button']"
            )

            btn_edit.click()
            # elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@data-testid='work-item-edit-form-button']")))
            # elem_edit = driver.find_element(By.XPATH, "//button[@data-testid='work-item-edit-button-sticky']")
            # elem_edit.click()

            time.sleep(1)
            
            write_log(f"       [Step 3] Updating database")
            
            # remove_label_needtotest(wait, url=issue_url_item)

            # # update db
            item = GitLab_Issue_Obj(id=0, project=project_item, path=path, test_state="Created", issue_test_url=issue_test_url, issue_test_number=issue_test_number, issue_number=iss_number_item, issue_url=issue_url_item, duedate=" "            
            )
            issue_obj_list.append(item)
            
            write_log(f"       ✓ Database record created")
            write_log(f"       ✓ Issue #{iss_number_item} completed successfully")
        
        except Exception as error:
            error_msg = f"{type(error).__name__} – {error}"
            write_log(f"   ✗ Error processing issue #{iss_number_item}: {error_msg}")
            print(f"Error: {error_msg}")
    
    write_log(f" --- Completed oncreate_testcase_update_issue_update_db ---")
    write_log(f" Total items added: {len(issue_obj_list)}")

def remove_label_needtotest(wait, url):
     
    write_log(f"     Attempting to remove 'Need to test' label")

    try:
        elem_needtotest = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='Need to test']/button")))
        elem_needtotest.click()
         
        write_log(f"     ✓ 'Need to test' label removed")
    except TimeoutException as ex:
         
        write_log(f"     ✗ Timeout removing label: {ex.msg}")
        try:
            slack_protocol.send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *Need_to_test*. :anger:\nPlease check this <{0}|issue>.""", url))
             
            write_log(f"     ✓ Slack notification sent")
        except Exception as slack_err:
             
            write_log(f"     ✗ Failed to send Slack: {slack_err}")

def onfinish_update_label_and_return_Query(driver, wait, issue_url_item, id):
     
    write_log(f" --- Starting onfinish_update_label_and_return_Query ---")
    write_log(f" Issue URL: {issue_url_item}")
    write_log(f" Issue ID: {id}")

    # update main issue
     
    write_log(f"     [Step 1] Loading issue and opening edit panel")

    driver.get(issue_url_item)
    time.sleep(3)
    elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@data-qa-selector='edit_link']")))
    driver.find_element(By.XPATH, "//button[@data-qa-selector='edit_link']").click() # Open textbox to input 
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//input[@aria-label='Search labels']")))
    elem_find_label = driver.find_element(By.XPATH, "//input[@aria-label='Search labels']")
    elem_find_label.click()

     
    write_log(f"     [Step 2] Adding 'Test Pass' label")

    elem_find_label.send_keys("Test Pass")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    write_log(f"     [Step 3] Adding 'wf:Ready_for_UAT' label")

    elem_find_label.send_keys("wf:Ready_for_UAT")
    elem_testcase = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='dropdown-item is-focused']")))
    time.sleep(1)
    elem_testcase.send_keys(Keys.SPACE)

    write_log(f"     [Step 4] Closing labels dropdown")

    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")))
    elem_close_asssign_label = driver.find_element(By.XPATH, "//button[@data-qa-selector='close_labels_dropdown_button']")
    elem_close_asssign_label.click()

    time.sleep(1)
    
    write_log(f"     [Step 5] Removing 'wf:QA' label")
    
    remove_label_qa(wait, issue_url_item)
    
    write_log(f"     [Step 6] Generating update query")

    # # return query
    query = """UPDATE ISSUE
SET test_state = 'Done'
WHERE id = {0};
""".format(id)
    
    write_log(f"     ✓ Update query generated")
    write_log(f"     --- Completed onfinish_update_label_and_return_Query ---")
    
    return query

def onfinish_add_desc_and_attach_file(driver, wait, test_issue_url, project, test_file_path):
     
    write_log(f" --- Starting onfinish_add_desc_and_attach_file ---")
    write_log(f" Test Issue URL: {test_issue_url}")
    write_log(f" Project: {project}")
    write_log(f" File Path: {test_file_path}")
    
    write_log(f"     [Step 1] Loading test issue page")

    driver.get(test_issue_url)
    driver.set_window_size(1047, 652)
    issue_test_desc = """Test Pass.

Please check the attach file for test result detail.

"""
    
     
    write_log(f"     [Step 2] Adding description")
    
    driver.find_element(By.ID, "note-body").send_keys(issue_test_desc)
    
     
    write_log(f"     [Step 3] Attaching file")
    
    bt_attach_file = driver.find_element(By.XPATH, "//button[@title='Attach a file or image']")
    bt_attach_file.click() # Attach file
    time.sleep(1)
    
     
    write_log(f"     [Step 3] Attaching file")
    
    bt_attach_file = driver.find_element(By.XPATH, "//button[@title='Attach a file or image']")
    bt_attach_file.click() # Attach file
    time.sleep(1)
    
     
    write_log(f"     [Step 3.1] Sending file path")
    
    pyautogui.write(test_file_path) 
    pyautogui.press('enter')

    time.sleep(3)
    
     
    write_log(f"     [Step 4] Submitting comment")
    
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-confirm btn-md gl-button split-content-button']")))
    elem.click()
    
     
    write_log(f"     [Step 4] Submitting comment")
    
    elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-confirm btn-md gl-button split-content-button']")))
    elem.click()

    write_log(f"     ✓ Comment submitted")
    write_log(f"     --- Completed onfinish_add_desc_and_attach_file ---")

def remove_label_qa(wait, url):
     
    write_log(f"     Attempting to remove 'wf:QA' label")
    
    try:
        elem_qa = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "//span[@data-qa-label-name='wf:QA']/button")))
        elem_qa.click()
         
        write_log(f"     ✓ 'wf:QA' label removed")
    except Exception as ex:
         
        write_log(f"     ✗ Error removing label: {type(ex).__name__} – {ex}")
        print("Remove label wf:QA, Exception: " + str(ex.msg))
        try:
            slack_protocol.send_survey(user="remove", text=str.format(""":speech_balloon: *Error* on *Remove* label *wf:QA*. :anger:\nPlease check this <{0}|issue>.""", url))
             
            write_log(f"     ✓ Slack notification sent")
        except Exception as slack_err:
             
            write_log(f"     ✗ Failed to send Slack: {slack_err}")
