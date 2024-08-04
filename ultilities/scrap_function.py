from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import logging
import traceback
from model import *
from ultilities.nameToId import *
logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

            # "id": self.id,
            # "comic_name": self.comic_name,
            # "hash_id": self.hash_id,
            # "other_name": self.other_name,
            # "img_src": self.img_src,
            # "author_name": self.author_name,
            # "status": self.status,
            # "kinds": self.kinds,
            # "comic_url": self.comic_url,
            # "view_count": self.view_count,
            # "comment": self.comment,
            # "love": self.love,
            # "newest_chapter": self.newest_chapter,
            # "updated_at": self.updated_at,
            # "chapters": [chapter.__dict__ for chapter in self.chapters]

def wait_for_parent_element(driver, parent_xpath, timeout=20):
    try:
        parent_element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, parent_xpath))
        )
        parent_element = driver.find_element(By.XPATH, parent_xpath)
        return parent_element
    except Exception as e:
        print(f"Error occurred while waiting for parent element: {e}")
        return None
    
    except Exception as e:
        print(f"Error occurred while waiting for {tag_name} attribute '{attribute_name}': {e}")
        return None
def wait_for_elememt_class_name(parent_element, class_name, timeout=20):
    try:
        element_class_name = WebDriverWait(parent_element, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )
        element_class_name = parent_element.find_element(By.CLASS_NAME, class_name)
        return element_class_name
    except Exception as e:
        print(f"Error occurred while waiting for parent element: {e}")
        return None
    
    except Exception as e:
        print(f"Error occurred while waiting for {tag_name} attribute '{attribute_name}': {e}")
        return None
def wait_for_element_tag_name(parent_element, tag_name, timeout=10):
    try:
        # Wait for the target element to be present within the parent element
        target_element = WebDriverWait(parent_element, timeout).until(
            EC.presence_of_element_located((By.TAG_NAME, tag_name))
        )
        target_element = parent_element.find_elements(By.TAG_NAME, tag_name)
        return target_element
    except Exception as e:
        print(f"Error occurred while waiting for {tag_name} attribute '{attribute_name}': {e}")
        return None

def scrap_list_comic_from_homepage(driver, parent_class, children_class, tag_name_of_target, img_src_base_if_need):

    XPATH_syntax = f"{parent_class}{children_class}"
    list_comic_homepage = []

    parent_container = wait_for_parent_element(driver, XPATH_syntax)

    # # comic_temps = parent_container.find_elements(By.TAG_NAME, tag_name_of_target)
    comic_temps = wait_for_element_tag_name(parent_container, tag_name_of_target)

    print(len(comic_temps))
    for index, comic_temp in enumerate(comic_temps):
        # img_src_div_parent = comic_temp.find_element(By.CLASS_NAME, 'book_avatar')
        img_src_parent_class = wait_for_elememt_class_name(comic_temp, 'book_avatar')

        # //div[contains(@class, 'list_grid_out')]

        img_src_text = img_src_parent_class.find_element(By.TAG_NAME, 'img').get_attribute('src')
        img_src_test = wait_for_element_tag_name(img_src_parent_class, 'img')
        img_src_test = img_src_test[0].get_attribute('src')
        # img_src_test = wait_for_element_tag_name(img_src_div_parent,'img').get_attribute('src')
        # ---------------------------------------------------------------------------------------------
        id = index + 1
        comic_name = comic_temp.find_element(By.XPATH, "//div[contains(@class, 'book_name')]").text
        hash_id = name_to_id(comic_name)
        other_name = ""
        # img_src = f'{img_src_base_if_need}{img_src_text}'

        print(img_src_test)


    return list_comic_homepage
