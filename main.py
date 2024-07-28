from seleniumbase import Driver
from selenium.webdriver.common.by import By
from model.ComicGeneralModel import ComicGeneral
from datetime import datetime
from model.ComicGeneralModel import ComicGeneral
from ultilities.saveCsv import write_comic_to_csv
from ultilities.nameToId import name_to_id
from ultilities.convertToCurrentTime import convertUpdateTimeToSec
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%m/%d/%Y")

ComicGeneralArr = []
for i in range(1, 2):
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

    for index,item in enumerate(items): 
        comic_general = item.find_elements(By.TAG_NAME, 'a')
        comic_general_url = item.find_elements(By.TAG_NAME, 'img')
        comic_name = comic_general[0].get_attribute('title').replace(',','.')
        comic_image_src = comic_general_url[0].get_attribute('src')
        comic_url =  comic_general[0].get_attribute('href')

        size = len(item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split())
        
        comic_viewCount, comic_comment, comic_love ="","",""

        if (size == 3):
            comic_viewCount, comic_comment, comic_love =  item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()
        if (size == 2):
            comic_viewCount, comic_comment =  item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()
        if (size == 1):
            comic_viewCount =  item.find_elements(By.CLASS_NAME, 'pull-left')[0].text.split()
        comic_viewCount = (comic_viewCount.replace(",","."))
        comic_comment = (comic_comment.replace(",","."))
        comic_love = (comic_love.replace(",","."))
        
        newest_chapter = comic_general[2].text
        updated_at = item.find_elements(By.CLASS_NAME, 'time')[0].text

        updated_at = convertUpdateTimeToSec(updated_at)

        

        id = name_to_id(comic_name)
        comicGeneral = ComicGeneral( id = name_to_id(comic_name),name = comic_name ,img_src = comic_image_src ,comic_url = comic_url,
                                    view_count = comic_viewCount ,comment = comic_comment,love =comic_love,
                                    newest_chapter =newest_chapter,updated_at = updated_at)
        if(len(ComicGeneralArr) == 0):
           write_comic_to_csv(comicGeneral)
           ComicGeneralArr.append(id)
        else:
            if (id in ComicGeneralArr):
                pass
            else:
                write_comic_to_csv(comicGeneral)
                ComicGeneralArr.append(id)
    driver.quit()