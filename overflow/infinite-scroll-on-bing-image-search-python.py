from selenium import webdriver
import time

driver = webdriver.Firefox()
driver.implicitly_wait(30)
verificationErrors = []
accept_next_alert = True

driver.get("http://www.bing.com/images/search?q=julia+roberts")
driver.find_element_by_link_text("All").click()

for i in range(1, 100):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)
    html_source = driver.page_source
    data = html_source.encode('utf-8')

