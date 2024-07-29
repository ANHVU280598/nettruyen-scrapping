import json
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from model.ComicGeneralJsonModel import ComicGeneral
from datetime import datetime
from ultilities.nameToId import name_to_id
from ultilities.convertToCurrentTime import convertUpdateTimeToSec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y")

ComicGeneralArr = []
comics = []

# Function to wait for an element and return it
def wait_for_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Element with {by}='{value}' not found within {timeout} seconds.")
        return None

for i in range(1, 680):
    page_index = ""
    if i != 1:
        page_index = "?page=" + str(i)

    ulr_tat_ca_truyen = "https://nettruyenaa.com/tim-truyen" + page_index
    ulr_truyen_moi = "https://nettruyenaa.com/tim-truyen?sort=15&status=&page=" + page_index
    url = ulr_tat_ca_truyen

    driver = Driver(uc=True)
    driver.uc_open_with_reconnect(url, 4)
    driver.sleep(3)

    items = driver.find_elements(By.CLASS_NAME, "item")

    for index, item in enumerate(items): 
        comic_general = item.find_elements(By.TAG_NAME, 'a')
        comic_general_url = item.find_elements(By.TAG_NAME, 'img')
        comic_name = comic_general[0].get_attribute('title').replace(',','.')
        comic_image_src = comic_general_url[0].get_attribute('src')
        comic_url = comic_general[0].get_attribute('href')

        size = len(item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split())

        comic_viewCount, comic_comment, comic_love = "", "", ""

        if size == 3:
            comic_viewCount, comic_comment, comic_love = item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()
        elif size == 2:
            comic_viewCount, comic_comment = item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()
        elif size == 1:
            comic_viewCount = item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()[0]

        comic_viewCount = comic_viewCount.replace(",", ".")
        comic_comment = comic_comment.replace(",", ".")
        comic_love = comic_love.replace(",", ".")

        newest_chapter = comic_general[2].text
        updated_at = item.find_elements(By.CLASS_NAME, 'time')[0].text

        updated_at = convertUpdateTimeToSec(updated_at)

        id = name_to_id(comic_name)

        comicGeneral = ComicGeneral(
            id=id,
            name=comic_name,
            img_src=comic_image_src,
            comic_url=comic_url,
            view_count=comic_viewCount,
            comment=comic_comment,
            love=comic_love,
            newest_chapter=newest_chapter,
            updated_at=updated_at,
        )

        if id not in ComicGeneralArr:
            comics.append(comicGeneral.to_dict())
            ComicGeneralArr.append(id)
    driver.quit()

# Write the comics data to a JSON file
    with open("comics.json", "w", encoding="utf-8") as json_file:
        json.dump(comics, json_file,ensure_ascii=False, indent=4)
    print("Data written to comics.json")
    store_page = "Data Store Page" + str(i)
    print(store_page)