from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from datetime import datetime

def write_log(message):
    """Helper function to write logs to file with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {message}\n"
    try:
        with open("collect-issue.log", "a", encoding="utf-8") as f:
            f.write(log_message)
    except Exception as e:
        print(f"Error writing to log file: {e}")


def get_gitlab_issue_info(driver, wait, project, new_issue_url, issue_link_list):
    """
    Thu thập thông tin các issue từ trang GitLab.

    Hàm này sẽ:
    - Đợi trang load xong container chứa danh sách issue.
    - Kiểm tra nếu xuất hiện thông báo "Sorry, your filter produced no results" thì kết thúc và không thu thập issue nào.
    - Nếu không có thông báo trên, sẽ lấy danh sách các issue hiện có và thêm vào issue_link_list.

    Tham số:
        driver: Đối tượng Selenium WebDriver.
        wait: Đối tượng WebDriverWait để chờ các phần tử xuất hiện.
        project: Tên dự án hiện tại.
        new_issue_url: Đường dẫn tạo issue mới.
        issue_link_list: Danh sách để lưu thông tin các issue thu thập được.

    Trả về:
        None. Kết quả được lưu vào issue_link_list.
    """
    write_log(f">>> Starting get_gitlab_issue_info for project: {project}")
    
    try:
        # Step 1: Wait for the page to be fully loaded
        write_log("  [Step 1] Waiting for issue list container to load...")
        wait.until(expected_conditions.presence_of_element_located(
          (By.XPATH, "//div[contains(@class, 'issuable-list-container')]")
        ))
        write_log("  ✓ Issue list container loaded successfully")
        
        # Step 2: Check for "No results" message
        write_log("  [Step 2] Checking for 'no results' message...")
        try:
          no_result_label = wait.until(expected_conditions.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Sorry, your filter produced no results')]")
          ))

          if no_result_label:
            write_log("  ⚠ No new issues found - filter produced no results")
            write_log(f"  Project '{project}' has no matching issues at this time")
            return
          
        except TimeoutException:
          write_log("  ✓ Issues exist - proceeding to extract information")
        
        # Step 3: Extract issue information
        write_log("  [Step 3] Extracting issue information...")
        initial_list_length = len(issue_link_list)
        
        try:
            elems = driver.find_elements(By.XPATH, "//div[contains(@class, 'issuable-list-container')]/ul/li")
            write_log(f"  Found {len(elems)} issue element(s)")
            
            for idx, li in enumerate(elems, 1):
                try:
                    att = li.get_attribute("data-qa-issuable-title")
                    tag_a = li.find_element(By.XPATH, ".//a[@class='gl-link issue-title-text']")
                    issue_url = tag_a.get_attribute("href")
                    issue_text = tag_a.get_attribute("text")
                    iss_number = issue_url[issue_url.rfind("/") + 1:]
                    
                    issue_link_list.append([iss_number, issue_url, project, new_issue_url, issue_text])
                    
                    write_log(f"    [{idx}] Issue #{iss_number}")
                    write_log(f"        Title: {issue_text}")
                    write_log(f"        URL: {issue_url}")
                    write_log(f"        Project: {project}")
                    
                except Exception as elem_error:
                    write_log(f"    ✗ Error processing issue element {idx}: {type(elem_error).__name__} – {elem_error}")
                    
        except TimeoutException as timeout_error:
            write_log(f"  ✗ TimeoutException while extracting issues: {timeout_error.msg}")
        except Exception as extraction_error:
            write_log(f"  ✗ Error during issue extraction: {type(extraction_error).__name__} – {extraction_error}")
        
        # Step 4: Summary
        newly_added = len(issue_link_list) - initial_list_length
        write_log(f"  [Step 4] Summary for project '{project}':")
        write_log(f"    - Issues added from this project: {newly_added}")
        write_log(f"    - Total issues in list: {len(issue_link_list)}")
        write_log(f">>> Completed get_gitlab_issue_info for project: {project}\n")
        
    except Exception as general_error:
        write_log(f"  ✗ CRITICAL ERROR in get_gitlab_issue_info: {type(general_error).__name__} – {general_error}")
        write_log(f">>> Failed to process project: {project}\n")
        raise
