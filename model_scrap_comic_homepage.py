import ultilities.helperFunction as helper
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time
import logging
from model.ComicHomePage import ComicHomePage
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
        driver = Driver(uc=True, headless=True)
        driver.uc_open_with_reconnect(base_url, 4)
        driver.sleep(3)
        helper.scroll_to_end_of_the_page(driver)

        comic_divs = driver.find_elements(By.XPATH, xPATH)

        for comic_div in comic_divs:
            try:
                name = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'fl-r')]//h3").text
                comic_url = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'fl-r')]//h3//a").get_attribute('href')
                description = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'fl-r')]//p").text
                no_chapter = comic_div.find_element(By.XPATH, ".//footer/div[1]/span[4]/span").text
                no_comment = comic_div.find_element(By.XPATH, ".//footer/div[1]/span[5]/span").text
                genere_temp = comic_div.find_elements(By.XPATH, ".//footer/div[2]/a")
                img_url = comic_div.find_element(By.XPATH, ".//div[contains(@class, 'fl-l')]//a//img").get_attribute('src')

                generes = [genere.text for genere in genere_temp]

                hash_id = helper.conver_comicName_to_hash(name)
                comicHomePage = ComicHomePage(
                    hash_id=hash_id,
                    name=name,
                    comic_url=comic_url,
                    description=description,
                    no_chapter=no_chapter,
                    no_comment=no_comment,
                    genres=generes,
                    img_url=img_url
                )
                helper.write_to_json(comicHomePage.to_dict(), 'blogtruyenHomePage.json')

            except Exception as e:
                logging.error(f"Error in process_comicHomePage at URL: base_url \n Hash_ID: {hash_id} \n{e}", exc_info=True)
                
        helper.clear_system_cache()

    except Exception as e:
        logging.error(f"Error in process_comicHomePage at URL: base_url \n Hash_ID: {hash_id} \n{e}", exc_info=True)


if __name__ == "__main__":
    # -----------------BLOG TRUYEN-----------------#
    base_url = "https://blogtruyen.vn"
    source = 'blogtruyen'
    noPage = 1649
    # XPATH for the outer div
    xPATH           = "//div[contains(@class, 'bg-white storyitem')]"
    name_path       = ".//div[contains(@class, 'fl-r')]//h3"
    comic_url_path  = ".//div[contains(@class, 'fl-r')]//h3//a"
    description     = ".//div[contains(@class, 'fl-r')]//p"
    no_chapter      = ".//footer/div[1]/span[4]/span"
    no_comment      = ".//footer/div[1]/span[5]/span"
    genere_temp     = ".//footer/div[2]/a"
    img_url         = ".//div[contains(@class, 'fl-l')]//a//img"
    # Multi thread

    max_threads = 2

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for i in range(1, noPage):
            page_index = "" if i == 0 else f"/page-{i}"
            url = f"{base_url}{page_index}"
            future = executor.submit(process_comicHomePage, url, xPATH)
            futures.append(future)

        # Optional: Handle results or exceptions if needed
        for future in as_completed(futures):
            try:
                future.result()  # Retrieve result or handle exceptions
            except Exception as e:
                logging.error(f"Error At line 85:  {url}: \n Error:  {e}")
    # -----------------END BLOG TRUYEN-----------------#


    


