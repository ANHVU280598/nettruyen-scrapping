import ultilities.helperFunction as helper
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time
import logging
from model.ComicDetail import ComicDetail
from concurrent.futures import ThreadPoolExecutor, as_completed
from ultilities.retryOnException import retry_on_exception


# Configure the logging to append to the log file if it exists
logging.basicConfig(filename='error_log_model_scrap_comic_homepage.log',
                    level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@retry_on_exception(retries=3, delay=2)
def process_comicHomePage(base_url, xPATH):
    try:
        print(base_url)
        driver = Driver(uc=True, headless=False)
        driver.uc_open_with_reconnect(base_url, 4)
        driver.sleep(3)
        helper.scroll_to_end_of_the_page(driver)

        comic_divs = driver.find_elements(By.XPATH, xPATH)

        for comic_div in comic_divs:
            try:
                try:
                    name = comic_div.find_element(By.XPATH, ".//h1[contains(@class, 'entry-title')]//a").text
                except Exception:
                    name = ""

                try:
                    descriptions = comic_div.find_elements(By.XPATH, ".//div[contains(@class, 'detail')]//div[contains(@class, 'content')]")
                except Exception:
                    descriptions = []

                try:
                    img_url = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'thumbnail')]//img").get_attribute('src')
                except Exception:
                    img_url = ""

                try:
                    no_chapter = comic_div.find_elements(By.XPATH, ".//div[contains(@class, 'list-chapters')]//div[contains(@class, 'list-wrap')]//p")
                except Exception:
                    no_chapter = []

                try:
                    views = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'description')]//span[contains(@id, 'PageViews')]").text
                except Exception:
                    views = ""

                try:
                    lastUpdate_temp = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'description')]//span[contains(@class, 'color-green')]").text
                except Exception:
                    lastUpdate_temp = ""

                try:
                    genere_temp = comic_div.find_elements(By.XPATH, ".//div[contains(@class, 'description')]//span[contains(@class, 'category')]")
                except Exception:
                    genere_temp = []

                try:
                    status = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'description')]//p[5]//span").text
                except Exception:
                    status = ""

                try:
                    author = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'description')]//p[1]//a").text
                except Exception:
                    author = ""

                try:
                    chapters = comic_div.find_elements(By.XPATH, ".//div[contains(@class, 'list-chapters')]//div[contains(@class, 'list-wrap')]//p//span[1]//a")
                except Exception:
                    chapters = []
                rating = 0
                other_name = []
                strings = []
                for des in descriptions:
                    strings.append(des.text)

                generes = []
                for genere in genere_temp:
                    generes.append(genere.text)
                
                

                hash_id = helper.conver_comicName_to_hash(name)
                description="".join(strings)
                lastUpdate = helper.convertStrTimeToSec(lastUpdate_temp)

                chapter_links = []
                for chapter in chapters:
                    chapter_links.append(chapter.get_attribute('href'))

                # Model
                comic = ComicDetail(
                    hash_id=hash_id,
                    comic_name=name,
                    img_src=img_url or "",
                    rating=rating or "",
                    view=views or "",
                    other_name=other_name or [],
                    genres=generes or [],
                    status=status or "",
                    author= author or "",
                    chapters = chapter_links or [],
                    lastUpdate = lastUpdate or 0,
                    description = description,
                    no_chapter = len(no_chapter) or 0,
                )
                helper.write_to_json(comic.to_dict(), 'blogTruyenDetail.json')


            except Exception as e:
                logging.error(f"Error in process_comicHomePage line 81 at URL: {base_url} \n Hash_ID: {hash_id} \n{e}", exc_info=True)
                
        helper.clear_system_cache()

    except Exception as e:
        logging.error(f"Error in process_comicHomePage line 86 at URL: {base_url} \n Hash_ID: {hash_id} \n{e}", exc_info=True)



if __name__ == "__main__":
    # -----------------BLOG TRUYEN-----------------#
    base_url = "https://blogtruyen.vn"
    source = 'blogtruyen'
    noPage = 1649
    # XPATH for the outer div
    xPATH           = "//section[contains(@class, 'manga-detail 2 bigclass ng-scope')]"
    name_path       = ".//div[contains(@class, 'fl-r')]//h3"
    comic_url_path  = ".//div[contains(@class, 'fl-r')]//h3//a"
    description     = ".//div[contains(@class, 'fl-r')]//p"
    no_chapter      = ".//footer/div[1]/span[4]/span"
    no_comment      = ".//footer/div[1]/span[5]/span"
    genere_temp     = ".//footer/div[2]/a"
    img_url         = ".//div[contains(@class, 'fl-l')]//a//img"
    # Multi thread

    # max_threads = 2

    # with ThreadPoolExecutor(max_workers=max_threads) as executor:
    #     futures = []
    #     for i in range(1, noPage):
    #         page_index = "" if i == 0 else f"/page-{i}"
    #         url = f"{base_url}{page_index}"
    #         future = executor.submit(process_comicHomePage, url, xPATH)
    #         futures.append(future)

    #     # Optional: Handle results or exceptions if needed
    #     for future in as_completed(futures):
    #         try:
    #             future.result()  # Retrieve result or handle exceptions
    #         except Exception as e:
    #             logging.error(f"Error At line 85:  {url}: \n Error:  {e}")

    test_url = "https://blogtruyen.vn/32253/sau-khi-bi-dung-si-cuop-di-moi-thu-toi-da-lap-to-doi-cung-voi-me-cua-dung-si"
    process_comicHomePage(test_url, xPATH )
                
    # -----------------END BLOG TRUYEN-----------------# 


    


