import json
import requests
import base64
import logging
import traceback
from typing import List
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from model.ComicModel import ComicGeneral, Chapter
from datetime import datetime
from ultilities.nameToId import name_to_id
from ultilities.convertToCurrentTime import convertUpdateTimeToSec
from urllib.parse import urlparse
from ultilities.saveJson import write_to_json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y")

def is_valid_https_url(url):
    https_pattern = r'^https://[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;%=]+$'
    return re.match(https_pattern, url) is not None

def get_image_in_chapter(chapter_url, driver):
    list_img_src = []
    try:
        driver.uc_open_with_reconnect(chapter_url, 4)
        page_chapters = driver.find_elements(By.CLASS_NAME, 'page-chapter')

        # Remove Ad Page
        remove_ad_page = page_chapters
        for link_img in remove_ad_page:
            img_src = link_img.find_element(By.TAG_NAME, 'img').get_attribute('data-original')
            list_img_src.append(img_src)
    except Exception:
        logging.error(f"Error on line {traceback.extract_stack()[-2].lineno} while getting images from chapter {chapter_url}")
    return list_img_src

def process_chapter(list_chapter_li):
    chapter_url = list_chapter_li.find_element(By.TAG_NAME, 'a').get_attribute('href')
    chapter_no = list_chapter_li.find_element(By.TAG_NAME, 'a').text
    chapter = None
    driver = None
    
    try:
        driver = Driver(uc=True)
        if is_valid_https_url(chapter_url):
            print(f"Chapter No: {chapter_no}, Chapter_Url: {chapter_url}")
            list_img_src = get_image_in_chapter(chapter_url, driver)
            
            chapter = Chapter(
                no_chapter=chapter_no,
                chapter_img=list_img_src
            )
        else:
            print(f"'{chapter_url}' is not a valid HTTPS URL.")
    except Exception:
        logging.error(f"Error on line {traceback.extract_stack()[-2].lineno} while processing chapter {chapter_url}")
    finally:
        if driver:
            driver.quit()
    return chapter

def scrap_eachChapter_Comic(url):
    driver = None
    list_chapters = []
    try:
        driver = Driver(uc=True)
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(3)
        detail_info = driver.find_element(By.CLASS_NAME, "detail-info")
        right_detail_info = detail_info.find_element(By.XPATH, "//div[contains(@class, 'col-xs-8') and contains(@class, 'col-info')]")

        # Author name, status, kinds
        author_name = right_detail_info.find_element(By.CLASS_NAME, "author").find_element(By.CLASS_NAME, "col-xs-8").text
        status = right_detail_info.find_element(By.CLASS_NAME, "status").find_element(By.CLASS_NAME, "col-xs-8").text
        kinds = right_detail_info.find_element(By.CLASS_NAME, "kind").find_element(By.CLASS_NAME, "col-xs-8").text.split('-')

        # Get List of Chapter And Link
        list_chapter_nav = driver.find_element(By.ID, "nt_listchapter").find_element(By.TAG_NAME, "nav")
        list_chapter_ul = list_chapter_nav.find_element(By.TAG_NAME, "ul")
        driver.execute_script("arguments[0].classList.add('active');", list_chapter_ul)
        list_chapter_lis = list_chapter_ul.find_elements(By.TAG_NAME, "li")

        # Extract and sort chapters based on chapter number
        chapters_data = []
        for list_chapter_li in list_chapter_lis:
            chapter_url = list_chapter_li.find_element(By.TAG_NAME, 'a').get_attribute('href')
            chapter_no = list_chapter_li.find_element(By.TAG_NAME, 'a').text
            chapters_data.append((chapter_no, list_chapter_li))

        # Sort chapters based on chapter number (ensure the format is numeric for correct sorting)

        # Use ThreadPoolExecutor to process chapters in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_chapter, li) for _, li in chapters_data]
            for future in as_completed(futures):
                chapter = future.result()
                if chapter:
                    list_chapters.append(chapter)

    finally:
        if driver:
            driver.quit()
    list_chapters.sort(key=lambda x: int(re.search(r'\d+', x.no_chapter)[0]), reverse=True)
    
    return list_chapters, author_name, status, kinds

def scrap_homepage(driver, url, index):
    try:
        driver.get(url)
        driver.sleep(3)
        item_parent = driver.find_element(By.CLASS_NAME, "items")
        item_child = item_parent.find_elements(By.CLASS_NAME, "item")
        for index, item_child_inner in enumerate(item_child):
            try:
                # id
                id = index + 1
                print(f"Comic Index: {id}")

                # comic_name
                comic_name = item_child_inner.find_element(By.TAG_NAME, 'figcaption').find_element(By.TAG_NAME, "h3").text
                print(f"Comic_name: {comic_name}")

                # hash_id
                hash_id = name_to_id(comic_name)
                print(f"Hash_id: {hash_id}")

                # img_src
                img_src = item_child_inner.find_element(By.CLASS_NAME, 'image').find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
                print(f"Comic Image Url: {img_src}")

                # comic_url
                comic_url = item_child_inner.find_element(By.CLASS_NAME, 'image').find_element(By.TAG_NAME, 'a').get_attribute('href')
                print(f"Comic Url: {comic_url}")

                # newest_chapter
                newest_chapter = item_child_inner.find_element(By.TAG_NAME, 'figcaption').find_element(By.CLASS_NAME, 'chapter').find_element(By.TAG_NAME, 'a').text
                updated_at = item_child_inner.find_element(By.TAG_NAME, 'figcaption').find_element(By.CLASS_NAME, 'chapter').find_element(By.TAG_NAME, 'i').text
                updated_at = convertUpdateTimeToSec(updated_at)
                print(f"newest_chapter: {newest_chapter} ; update_at: {updated_at}")

                # Update when it available
                view_count = ""
                comment = ""
                love = ""
                other_name = ""

                # Get List of Chapter with contain Chapter No + Chapter Img Url
                list_chapters, author_name, status, kinds = scrap_eachChapter_Comic(comic_url)

                comicModel = ComicGeneral(
                    id=id,
                    comic_name=comic_name,
                    hash_id=hash_id,
                    other_name=other_name,
                    author_name=author_name,
                    status=status,
                    kinds=kinds,
                    img_src=img_src,
                    comic_url=comic_url,
                    view_count=view_count,
                    comment=comment,
                    love=love,
                    newest_chapter=newest_chapter,
                    updated_at=updated_at,
                    chapters=list_chapters,
                )

                comic_data_dict = comicModel.to_dict()
                write_to_json(comic_data_dict)
            except Exception:
                logging.error(f"Error on line {traceback.extract_stack()[-2].lineno} while processing comic item")
    except Exception:
        logging.error(f"Error on line {traceback.extract_stack()[-2].lineno} while scraping homepage {url}")