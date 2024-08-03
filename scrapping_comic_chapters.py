import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from readJsonFile import read_json_file
from seleniumbase import Driver
from model.ComicChaptersJsonModel import ComicChapterModel, Chapter
from typing import List
import requests
import base64
import requests
import base64
import logging

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def image_url_to_base64(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        img_data = response.content  # Get the binary data
        img_base64 = base64.b64encode(img_data).decode('utf-8')  # Convert to Base64
        return img_base64
    except Exception as e:
        logging.error(f"Error converting image URL to Base64: {url} - {e}")
        return None

def extract_info_from_chapter_page(driver, chapters: List[str]) -> List[Chapter]:
    list_chapters = []

    for index, chapter_url in enumerate(chapters):
        chapter_url = chapters[index]
        chapter_no = index + 1

        try:
            driver.get(chapter_url)
            driver.implicitly_wait(5)
            page_chapters = driver.find_elements(By.CLASS_NAME, 'page-chapter')

            img_url_list = []
            for img_url in page_chapters:
                url = img_url.find_element(By.TAG_NAME, 'img')
                get_img_url = url.get_attribute("data-src")
                img_base64 = image_url_to_base64(get_img_url)
                img_url_list.append(img_base64)

            chapter = Chapter(
                number=chapter_no,
                img_source=img_url_list
            )
            list_chapters.append(chapter)

        except Exception as e:
            logging.error(f"Error extracting chapter info from {chapter_url}: {e}")

    return list_chapters

def open_browser_in_headless_mode():
    file_path = 'comics.json'
    comic_infos = read_json_file(file_path)

    # Get the URL from the first comic entry
    for url_detail in comic_infos:
        id = url_detail.id
        url = url_detail.comic_url
        print(url)

        # Set up the driver using seleniumbase with headless mode enabled
        driver = Driver(uc=True)
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(3)

        
        try:
            # Extract details from the left table
            detail_info = driver.find_elements(By.CLASS_NAME, 'detail-info')
            ul_list_info = detail_info[0].find_elements(By.CLASS_NAME, 'list-info')
            lists = ul_list_info[0].find_elements(By.CLASS_NAME, 'col-xs-8')
            
            # lists = lists[::-1]
            # a = ul_list_info[0].find_element(By.CLASS_NAME, "othername").text
         

            # Initialize variables to hold the comic information
            different_name = ""
            author = ""
            status = ""
            kinds = []
            view_count = ""

            try:
                different_name = ul_list_info[0].find_element(By.CLASS_NAME, "othername").find_element(By.CLASS_NAME, 'col-xs-8').text
            except Exception as e:
                logging.error(f"Error extracting different_name: {e}")

            try:
                author = ul_list_info[0].find_element(By.CLASS_NAME, "author").find_element(By.CLASS_NAME, 'col-xs-8').text
            except Exception as e:
                logging.error(f"Error extracting author: {e}")

            try:
                status = ul_list_info[0].find_element(By.CLASS_NAME, "status").find_element(By.CLASS_NAME, 'col-xs-8').text
            except Exception as e:
                logging.error(f"Error extracting status: {e}")

            try:
                kind_str = ul_list_info[0].find_element(By.CLASS_NAME, "kind").find_element(By.CLASS_NAME, 'col-xs-8').text
                kinds = kind_str.split('-')
            except Exception as e:
                logging.error(f"Error extracting kinds: {e}")

            try:
                view_count = ul_list_info[0].find_element(By.CLASS_NAME, "row").find_element(By.CLASS_NAME, 'col-xs-8').text
            except Exception as e:
                logging.error(f"Error extracting view_count: {e}")

            print(f"Different Name: {different_name}")
            print(f"Author: {author}")
            print(f"Status: {status}")
            print(f"Kinds: {kinds}")
            print(f"View Count: {view_count}")

            # Extract chapter information
            list_chapter = driver.find_element(By.ID, "nt_listchapter")
            desc = list_chapter.find_element(By.ID, "desc")
            driver.execute_script("arguments[0].classList.add('active');", desc)

            rows = desc.find_elements(By.CLASS_NAME, "row")
            chapters = [row.find_element(By.TAG_NAME, "a").get_attribute("href") for row in rows]

            # Extract and store chapter information
            list_chapters = extract_info_from_chapter_page(driver, chapters)

            # Initialize the ComicChapterModel with the extracted data
            comic_chapter_model = ComicChapterModel(
                id=id,
                name="",
                different_name=different_name,
                author=author,
                status=status,
                kinds=kinds,
                view_count=view_count,
                img_src="",
                chapters=list_chapters
            )

            # Convert the model to a dictionary and then to JSON
            comic_data_dict = comic_chapter_model.to_dict()
            json_output = json.dumps(comic_data_dict, ensure_ascii=False, indent=4)
            
            # Save the JSON to a file
            with open('comic_chapter_data.json', 'w', encoding="utf-8") as json_file:
                json_file.write(json_output)

            print("Comic data has been saved to comic_chapter_data.json")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

        finally:
            print("Script finished. The browser will remain open.")
            input("Press Enter to close the browser...")
            driver.quit()

# Example usage
open_browser_in_headless_mode()