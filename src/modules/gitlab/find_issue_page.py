from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException


def get_gitlab_issue_info(driver, wait, project, new_issue_url):
    print(">Get Gitlab Issue Information")
    issue_link_list = []
    try:
      elem = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//ul[@class='content-list issuable-list issues-list']/li")))
      # print(">>>>elem: ", elem)
      elems = driver.find_elements(By.XPATH, "//div[@class='issuable-list-container']/ul/li")
    #   print(">>>>elems: ", elems)
      for li in elems:
        # print('>>>li', li)
        att = li.get_attribute("data-qa-issuable-title")
        # print('>>>att li', att)
        tag_a = li.find_element(By.XPATH, ".//a[@class='gl-link issue-title-text']")
        # print(">>>>tag_a: ", tag_a)
        issue_url = tag_a.get_attribute("href")
        issue_text = tag_a.get_attribute("text")
        # print(">>>>url: ", issue_url)
        # print(">>>>text: ", issue_text)
        iss_number = issue_url[issue_url.rfind("/") + 1:]
        # print(">>>>iss Number: ", iss_number)
        issue_link_list.append([iss_number, issue_url, project, new_issue_url, issue_text])
      # print(">>>>issue_link_list: ", issue_link_list)
    except TimeoutException as ex:
      print("TimeoutException has been thrown. " + str(ex.msg))
      # send_survey(user="get", text=""":interrobang::interrobang::interrobang: *Error* on *Get Gitlab Issue Information.* :broken_heart::broken_heart::broken_heart:\nPlease get help from your Administrator.""")
    print("project issue_link_list. len ", len(issue_link_list))
    return issue_link_list
