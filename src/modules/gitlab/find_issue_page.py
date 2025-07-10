from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException


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
    print(">Get Gitlab Issue Information")
    # Wait for the page to be fully loaded by checking for the presence of the main container
    wait.until(expected_conditions.presence_of_element_located(
      (By.XPATH, "//div[contains(@class, 'issuable-list-container')]")
    ))
    try:
      # Select and click "New task" option
      no_result_label = wait.until(expected_conditions.presence_of_element_located(
        (By.XPATH, "//h1[contains(text(),'Sorry, your filter produced no results')]")
      ))

      if no_result_label:
        print(">>>No new issue")
        return
      
    except TimeoutException as ex:
      print(">>>New issue exists")
      
    try:
        elems = driver.find_elements(By.XPATH, "//div[@class='issuable-list-container']/ul/li")
        for li in elems:
          att = li.get_attribute("data-qa-issuable-title")
          tag_a = li.find_element(By.XPATH, ".//a[@class='gl-link issue-title-text']")
          issue_url = tag_a.get_attribute("href")
          issue_text = tag_a.get_attribute("text")
          iss_number = issue_url[issue_url.rfind("/") + 1:]
          issue_link_list.append([iss_number, issue_url, project, new_issue_url, issue_text])
    except TimeoutException as ex:
      print("TimeoutException has been thrown. " + str(ex.msg))
    print("project issue_link_list. len ", len(issue_link_list))
