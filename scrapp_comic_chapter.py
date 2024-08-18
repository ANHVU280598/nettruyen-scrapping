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
from model.ComicChapters import Chapter, ComicChapters
from datetime import datetime

@retry_on_exception(retries=3, delay=2)
def scroll_to_end_of_the_page(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = total_height / 5
    for i in range(5):
        driver.execute_script(f"window.scrollTo(0, {scroll_increment * (i + 1)});")
        time.sleep(2)

@retry_on_exception()
def process_manga_chapter(index, each_manga):
    no_chapter = each_manga.find_element(By.TAG_NAME, 'a').text
    chapter_url = each_manga.find_element(By.TAG_NAME, 'a').get_attribute('href')
    chapter_title, chapter_img = process_comic_chapters(chapter_url)

    return index, Chapter(
        no_chapter=no_chapter,
        chapter_title=chapter_title,
        chapter_img=chapter_img,
        updated_at= datetime.now().strftime('%B %d, %Y - %I:%M %p')
    )

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




@retry_on_exception(retries=3, delay=2)
def process_manhwaclan(url, hash_id):
    driver = Driver(uc=True, headless=True)
    print(url)
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

        list_manga_li = driver.find_elements(By.XPATH, "//li[contains(@class, 'wp-manga-chapter')]")


        chapters = [None] * len(list_manga_li)
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_manga_chapter, idx, each_manga): idx for idx, each_manga in enumerate(list_manga_li)}
            for future in as_completed(futures):
                idx, chapter = future.result()
                chapters[idx] = chapter
                print(f"Chapter {idx} done")

    finally:
        driver.quit()


    comic_chapter = ComicChapters(
        hash_id = hash_id,
        chapters = chapters
    )
    write_to_json(comic_chapter.to_dict(), 'comic_chapters.json')
    return chapters


if __name__ == "__main__":
    datas = read_json_file('comic_name.json')
    for data in datas:
        process_manhwaclan(data.comic_url, data.hash_id)
        print(f"done: {data.hash_id}")