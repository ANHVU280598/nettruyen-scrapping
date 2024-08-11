from seleniumbase import Driver
from selenium.webdriver.common.by import By
from ultilities.nameToId import name_to_id
from model.ComicModel import ComicGeneral, Chapter
import time
import json
import traceback
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from ultilities.saveJson import write_to_json
# Configure logging
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, format='%(message)s')

def retry_on_exception(retries=5, delay=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error at {func.__name__}, attempt {attempt + 1}/{retries}: {e}")
                    time.sleep(delay)
            raise
        return wrapper
    return decorator

@retry_on_exception()
def process_manga_chapter(index, each_manga):
    no_chapter = each_manga.find_element(By.TAG_NAME, 'a').text
    chapter_url = each_manga.find_element(By.TAG_NAME, 'a').get_attribute('href')
    chapter_title, chapter_img = process_comic_chapters(chapter_url)
    return index, Chapter(
        no_chapter=no_chapter,
        chapter_title=chapter_title,
        chapter_img=chapter_img
    )

@retry_on_exception()
def scroll_to_end_of_the_page(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = total_height / 5
    
    for i in range(5):
        driver.execute_script(f"window.scrollTo(0, {scroll_increment * (i + 1)});")
        time.sleep(2)

@retry_on_exception()
def append_new_data(comicModel):
    
    # file_path = 'comica.json'
    # try:
    #     with open(file_path, 'r') as file:
    #         data = json.load(file)
    # except FileNotFoundError:
    #     data = []

    # data.append(comicModel.to_dict())
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     json.dump(data, file, indent=4, ensure_ascii=False)
    try:
        file_path = 'comics.json'
        write_to_json(comicModel, file_path)
    except Exception as e:
        print(f'Something Wrong in Append_New_Data')
    print("Successful add New Comic")

@retry_on_exception()
def process_comic_chapters(url):
    driver = Driver(uc=True, headless=True)
    chapter_title = None
    chapter_imgs = []
    print(f"Process comic chapter: {url}")
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(1)

        scroll_to_end_of_the_page(driver)

        chapter_title = driver.find_element(By.XPATH, "//h1[contains(@id, 'chapter-heading')]").text
        chapter_imgs = driver.find_elements(By.XPATH, "//div[contains(@class, 'page-break no-gaps')]")

        chapter_img_list = []
        for chapter_img in chapter_imgs:
            chapter_img_url = chapter_img.find_element(By.TAG_NAME, 'img').get_attribute('src')
            chapter_img_list.append(chapter_img_url)

    finally:
        driver.quit()

    return chapter_title, chapter_img_list

@retry_on_exception()
def process_comic(url):
    driver = Driver(uc=True, headless=True)
    other_name = ''
    author_name = ''
    status = ''
    kinds = []
    chapters = []
    print(f"Process comic Url: {url}")
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(1)

        try:
            manhwaclan_add_class_name = driver.find_element(By.XPATH, "//ul[contains(@class,'main version-chap no-volumn active')]")
            driver.execute_script("arguments[0].classList.add('loaded');", manhwaclan_add_class_name)
            driver.execute_script("arguments[0].style.maxHeight = '100%';", manhwaclan_add_class_name)
        except Exception:
            logging.info("No need to add class if not too many chapters")

        scroll_to_end_of_the_page(driver)

        post_content_items = driver.find_elements(By.XPATH, "//div[contains(@class, 'post-content_item')]")
        for post_content_item in post_content_items:
            post_content_item_title = post_content_item.find_element(By.TAG_NAME, 'h5').text
            post_content_item_detail = post_content_item.find_element(By.CLASS_NAME, 'summary-content').text
            if post_content_item_title == "Alternative":
                other_name = post_content_item_detail
            elif post_content_item_title == "Genre(s)":
                kinds = post_content_item_detail.split(',') if ',' in post_content_item_detail else [post_content_item_detail]
            elif post_content_item_title == "Status":
                status = post_content_item_detail

        list_manga_li = driver.find_elements(By.XPATH, "//li[contains(@class, 'wp-manga-chapter')]")

        chapters = [None] * len(list_manga_li)

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(process_manga_chapter, idx, each_manga): idx for idx, each_manga in enumerate(list_manga_li)}
            for future in as_completed(futures):
                idx, chapter = future.result()
                chapters[idx] = chapter
                print(f"Chapter {idx} done")

    finally:
        driver.quit()
    
    return other_name, author_name, status, kinds, chapters

def scrapp_comics(url):
    driver = Driver(uc=True, headless=True)
    
    try:
        driver.uc_open_with_reconnect(url, 4)
        driver.sleep(1)
        scroll_to_end_of_the_page(driver)

        comic_loop = driver.find_elements(By.XPATH, "//div[contains(@class, 'page-item-detail manga ')]")
        for index, manga in enumerate(comic_loop):
            id = index
            comic_name = manga.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text
            hash_id = name_to_id(comic_name)
            img_src = manga.find_element(By.TAG_NAME, 'img').get_attribute('src')
            comic_url = manga.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
            view_count = 0
            comment = 0
            parent_rating = manga.find_element(By.CLASS_NAME, 'post-total-rating')
            rating = parent_rating.find_element(By.TAG_NAME, 'span').text

            parent_chapter = manga.find_element(By.CLASS_NAME, 'list-chapter')
            newest_chapter = parent_chapter.find_element(By.TAG_NAME, 'span').text
            print(f"ID: {id}")
            print(f"Comic Name: {comic_name}")
            print(f"Hash ID: {hash_id}")
            print(f"Image Source: {img_src}")
            print(f"Comic URL: {comic_url}")
            print(f"View Count: {view_count}")
            print(f"Comment: {comment}")
            print(f"Rating: {rating}")
            print(f"Newest Chapter: {newest_chapter}")

            other_name, author_name, status, kinds, list_chapters = process_comic(comic_url)

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
                rating=rating,
                newest_chapter=newest_chapter,
                chapters=list_chapters,
            )

            append_new_data(comicModel)
                
    finally:
        driver.quit()

if __name__ == "__main__":
    target_url = 'https://manhwaclan.com/'
    scrapp_comics(target_url)