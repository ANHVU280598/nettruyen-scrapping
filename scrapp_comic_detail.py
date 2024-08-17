from ultilities.readJsonFile import read_json_file
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
import re
from model.ComicDetail import ComicDetail
from concurrent.futures import ThreadPoolExecutor, as_completed
from ultilities.retryOnException import retry_on_exception

def extract_view_from_a_string(txt):
    match = re.search(r'\b(\d+\.?\d*)\b', txt)

    if match:
        # Extract the number as a string
        number_str = match.group(1)
        # Convert to a float
        number = float(number_str)
        return number
    else:
        return ""

@retry_on_exception(retries=3, delay=2)
def process_manhwaclan(hash_id, comic_name, comic_url):
    driver = Driver(uc=True, headless=True)
    try:
        driver.uc_open_with_reconnect(comic_url, 4)
        driver.sleep(3)

        comic_img_parent = driver.find_element(By.XPATH, "//div[contains(@class, 'summary_image')]")


        status_parent = driver.find_element(By.XPATH, "//div[contains(@class, 'post-status')]")


        post_content_parent = driver.find_element(By.XPATH, "//div[contains(@class, 'post-content')]")

        rating_parent = post_content_parent.find_element(By.CLASS_NAME, "post-total-rating")


        post_content_item = post_content_parent.find_elements(By.CLASS_NAME, "post-content_item")

        view = post_content_item[1].find_element(By.CLASS_NAME, 'summary-content').text


        other_name = post_content_item[2].find_element(By.CLASS_NAME, 'summary-content').text


        genre = post_content_item[3].find_element(By.CLASS_NAME, 'summary-content').text


        # Data
        img_src = comic_img_parent.find_element(By.TAG_NAME, 'img').get_attribute('src')
        status = status_parent.find_element(By.CLASS_NAME, "summary-content").text
        rating = rating_parent.find_element(By.TAG_NAME, 'span').text
        view = str(extract_view_from_a_string(view))
        other_name = other_name.split('/')
        genre = genre.split(',')

        # Model
        comic = ComicDetail(
            hash_id=hash_id,
            comic_name=comic_name,
            img_src=img_src or "",
            rating=rating or "",
            view=view or "",
            other_name=other_name or [],
            genres=genre or [],
            status=status or "",
        )

        write_to_json(comic.to_dict(), "comic_detail.json")



    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    data = read_json_file('comic_name.json')


    max_threads = 5  # Adjust based on your needs

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for index, comic in enumerate(data):
            hash_id = comic.hash_id
            comic_name = comic.comic_name
            comic_url = comic.comic_url
            future = executor.submit(process_manhwaclan, hash_id, comic_name, comic_url)
            futures.append(future)

        # Optional: Handle results or exceptions if needed
        for future in as_completed(futures):
            try:
                future.result()  # Retrieve result or handle exceptions
            except Exception as e:
                logging.error(f"An error occurred: {e}")

