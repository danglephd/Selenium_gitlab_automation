import os

from .signin_page import gitlabsignin
from ..db import firebase
from .update_testcase_page import onfinish_update_label_and_return_Query, onfinish_add_desc_and_attach_file

from dotenv import load_dotenv

from ..slack import slack_protocol

try:
  load_dotenv()
  GITLAB_USERNAME = os.environ["GITLAB_USERNAME"]
  GITLAB_PASSWORD = os.environ["GITLAB_PASSWORD"]
  TEST_ISSUE_TEMP = os.environ["TEST_ISSUE_TEMP"]
  TEST_ISSUE_FOLDER_TEMP = os.environ["TEST_ISSUE_FOLDER_TEMP"]
  TEST_ISSUE_DESC_TEMP = os.environ["TEST_ISSUE_DESC_TEMP"]
  TEST_ISSUE_FILE_TEMP = os.environ["TEST_ISSUE_FILE_TEMP"]
  
  SIGN_IN_URL = os.environ["SIGN_IN_URL"]

  # print("Environment variable>>> ", TEST_ISSUE_TEMP, TEST_ISSUE_DESC_TEMP)

except  Exception as error:
  print("Main, Environment variable does not exist: ",  type(error).__name__, "–", error)

def collect_finish_gitlab_issues(issue_finished_list):
    
    # # SQLitedb
    # criteria = "WHERE test_state LIKE 'Finish'"
    # issue_list = sqlite.getListIssue(criteria)

    # Firebasedb
    criteria = ['test_state', 'IN', ['Finish']]
    issue_list = firebase.getListIssue2(criteria)

    if len(issue_list) > 0:
      for item in issue_list:
        issue_finished_list.append(item)

def finish_testcase(driver, wait):
    print("RPA finish_testcase")
    issue_finished_list = []
    issue_finished_success_list = []
    collect_finish_gitlab_issues(issue_finished_list)
    if(len(issue_finished_list) > 0):
      gitlabsignin(driver, SIGN_IN_URL, GITLAB_USERNAME, GITLAB_PASSWORD)
      for row in issue_finished_list:
        # id, project, path, test_state, issue_test_url, issue_test_number, issue_number, issue_url
        
        isValidFile = checkFileIsValid(row.path)
        # Kiểm tra file ở row.path nếu kích thước < 10 MB thì  
        if isValidFile:
          onfinish_add_desc_and_attach_file(driver, wait, test_issue_url=row.issue_test_url, project=row.project, test_file_path=row.path)
          query = onfinish_update_label_and_return_Query(driver, wait, issue_url_item=row.issue_url, id=row.id)
          issue_finished_success_list.append(row)
          firebase.update_issue_test_state(row.id, 'Done')
        else :
           # Nếu file không hợp lệ thì gửi thông báo lỗi qua Slack
           slack_protocol.send_survey(user="file_error", text=str.format(""":speech_balloon: *Error* on *Attach file* (file not exist or too large). :anger:\nPlease check this <{0}|issue>. Path at: <{1}>""", row.issue_url, row.path))
    if len(issue_finished_success_list) > 0:
      slack_protocol.send_survey(user="AAAA", block=slack_protocol.read_blocks([], issue_finished_success_list, is_finishing=True, is_creating=False), text="Selenium result")
    else:
      slack_protocol.send_survey(user="no_success", text=":speech_balloon: No issues were successfully finished due to file errors or no issues found.")

def checkFileIsValid(file_path):
    """
    Kiểm tra file có tồn tại và kích thước nhỏ hơn 10MB.

    Args:
        file_path (str): Đường dẫn đến file cần kiểm tra

    Returns:
        bool: True nếu file tồn tại và kích thước < 10MB, False trong các trường hợp còn lại
    """
    try:
        if not file_path or not os.path.isfile(file_path):
            print(f"File không tồn tại: {file_path}")
            return False
            
        max_size = 10 * 1024 * 1024  # 10MB
        file_size = os.path.getsize(file_path)
        
        is_valid = file_size < max_size
        if not is_valid:
            print(f"File quá lớn ({file_size / (1024*1024):.2f}MB): {file_path}")
            
        return is_valid
        
    except Exception as e:
        print(f"Lỗi khi kiểm tra file: {str(e)}")
        return False