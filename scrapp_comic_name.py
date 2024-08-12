from seleniumbase import Driver
from selenium.webdriver.common.by import By
from ultilities.nameToId import name_to_id
import time
import json
import traceback
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from ultilities.saveJson import write_to_json
from model.ComicName import ComicName
from ultilities.retryOnException import retry_on_exception

logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(message)s')



@retry_on_exception(retries=3, delay=2)
def scroll_to_end_of_the_page(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = total_height / 5
    for i in range(5):
        driver.execute_script(f"window.scrollTo(0, {scroll_increment * (i + 1)});")
        time.sleep(2)

@retry_on_exception(retries=3, delay=2)
def get_comic_name(url, source):
    print(url)
    driver = Driver(uc=True, headless=True)
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(3)
        scroll_to_end_of_the_page(driver)
        comic_names = driver.find_elements(By.XPATH, "//div [contains(@class, 'post-title font-title')]")
        for comic_name in comic_names:
            try: 
                name = comic_name.find_element(By.TAG_NAME, 'a').text
                comic_url = comic_name.find_element(By.TAG_NAME, 'a').get_attribute('href')
                hash_id = name_to_id(name)
                if name is not None and name != "":
                    comic_name_model = ComicName(
                        hash_id = hash_id,
                        comic_name = name ,
                        comic_url = comic_url,
                        source = source
                    )
                    write_to_json(comic_name_model.to_dict(), 'comic_name.json')
            except Exception as e:
                logging.info(f"Errors: {e}")
    except Exception as e:
        logging.info(f"Errors: {e}")
    finally:
        driver.quit()




# Manhwaclan website
def process_manhwaclan():
    base_url = "https://manhwaclan.com"
    source = 'manhwaclan'
    max_threads = 10  # Adjust based on your needs

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for i in range(1, 170):
            page_index = "" if i == 1 else f"/page/{i}/"
            url = f"{base_url}{page_index}"
            future = executor.submit(get_comic_name, url, source)
            futures.append(future)

        # Optional: Handle results or exceptions if needed
        for future in as_completed(futures):
            try:
                future.result()  # Retrieve result or handle exceptions
            except Exception as e:
                logging.error(f"An error occurred: {e}")



if __name__ == "__main__":

    process_manhwaclan()