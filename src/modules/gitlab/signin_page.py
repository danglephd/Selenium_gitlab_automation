from selenium.webdriver.common.by import By

def gitlabsignin(driver, SIGN_IN_URL, GITLAB_USERNAME, GITLAB_PASSWORD):
    print("gitlabsignin")
    driver.get(SIGN_IN_URL)
    driver.maximize_window()
    driver.find_element(By.ID, "user_login").send_keys(GITLAB_USERNAME)
    driver.find_element(By.ID, "user_password").send_keys(GITLAB_PASSWORD)
    submit_ele = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_ele.click()