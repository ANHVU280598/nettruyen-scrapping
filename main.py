from seleniumbase import Driver
from selenium.webdriver.common.by import By

driver = Driver(uc=True)
driver.uc_open_with_reconnect("https://nettruyenviet.com/", 4)
driver.sleep(3)


items = driver.find_elements(By.CLASS_NAME, "item")

for item in items:
    print(item.text)

driver.quit()