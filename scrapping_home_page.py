import json
import requests
import base64
import logging
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from model.ComicGeneralJsonModel import ComicGeneral
from datetime import datetime
from ultilities.nameToId import name_to_id
from ultilities.convertToCurrentTime import convertUpdateTimeToSec

# Configure logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y")

ComicGeneralArr = []
comics = []

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

def process_page(driver, url, page_index):
    driver.get(url)
    driver.sleep(3)

    items = driver.find_elements(By.CLASS_NAME, "item")

    for index, item in enumerate(items): 
        try:
            comic_general = item.find_elements(By.TAG_NAME, 'a')
            comic_general_url = item.find_elements(By.TAG_NAME, 'img')
            comic_name = comic_general[0].get_attribute('title').replace(',', '.')
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

            hash_id = name_to_id(comic_name)
            comic_image_src_v1 = image_url_to_base64(comic_image_src)

            comicGeneral = ComicGeneral(
                hash_id=hash_id,
                id=index,
                name=comic_name,
                img_src=comic_image_src_v1,
                comic_url=comic_url,
                view_count=comic_viewCount,
                comment=comic_comment,
                love=comic_love,
                newest_chapter=newest_chapter,
                updated_at=updated_at,
            )

            if hash_id not in ComicGeneralArr:
                comics.append(comicGeneral.to_dict())
                ComicGeneralArr.append(hash_id)

        except Exception as e:
            logging.error(f"Error processing comic item: {e}")

def main():
    driver = Driver(uc=True)

    try:
        for i in range(1, 680):
            page_index = "" if i == 1 else f"?page={i}"
            url = f"https://nettruyenaa.com/tim-truyen{page_index}"

            process_page(driver, url, i)

            print(f"Data Store Page {i}")

    finally:
        driver.quit()
        with open("comics.json", "w", encoding="utf-8") as json_file:
            json.dump(comics, json_file, ensure_ascii=False, indent=4)
        print("Data written to comics.json")

if __name__ == "__main__":
    main()