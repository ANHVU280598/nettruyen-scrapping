from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from readJsonFile import read_json_file

def open_browser_in_headless_mode():
 
    url = "https://nettruyenaa.com/truyen-tranh/moi-tinh-dau-dang-ghet-14760"
 

    # Set up Chrome options to run in headless mode
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the driver with options for Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.implicitly_wait(3)


    # banner_text_center = driver.find_element(By.ID, "pop_nettruyenaa")
    # driver.execute_script("arguments[0].style.display = 'none';", banner_text_center)
    # # banner_text_center.click()


    # ads = driver.find_elements(By.CLASS_NAME, "wap_bottombanner")
    # for ad in ads:
    #     driver.execute_script("arguments[0].style.display = 'none';", ad)

    # ad_banners = driver.find_elements(By.CLASS_NAME, "ads-banner")
    # for ad in ad_banners:
    #     driver.execute_script("arguments[0].style.display = 'none';", ad)


    list_chapter = driver.find_element(By.ID, "nt_listchapter")
    desc = list_chapter.find_element(By.ID, "desc")
    driver.execute_script("arguments[0].classList.add('active');", desc)
    # print(list_chapter.text)
 
    # modal = driver.find_element(By.ID, "myModal")
    # driver.execute_script("arguments[0].style.display = 'none';", modal)


    # main = driver.find_element(By.TAG_NAME, "main")
    # driver.execute_script("arguments[0].style.display = 'none';", containers[0])
    # main.click()
    # print(banner_text_center.text)

    print("Script finished. The browser will remain open.")
    input("Press Enter to close the browser...")
    driver.quit()

# Example usage
open_browser_in_headless_mode()