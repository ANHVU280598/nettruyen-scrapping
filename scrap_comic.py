from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def force_load_images(url):
    # Initialize the Driver
    driver = Driver(uc=True)
    
    try:
        # Get the total scroll height
        total_height = driver.execute_script("return document.body.scrollHeight")
        
        # Calculate the increment for scrolling (20 parts)
        scroll_increment = total_height / 20
        
        # Scroll through the page in increments
        for i in range(20):
            driver.execute_script(f"window.scrollTo(0, {scroll_increment * (i + 1)});")
            time.sleep(1)  # Wait for new images to load
        
        
        # Wait for images to be fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'img'))
        )
        
        ul = driver.find_element(By.CLASS_NAME, 'list_grid')
        li = ul.find_elements(By.TAG_NAME, 'li')
        # Retrieve all image sources after forcing load
        for index, a in enumerate(li):
            
            a = a.find_element(By.TAG_NAME, 'a')
            src = a.find_element(By.TAG_NAME, 'img').get_attribute('src')
            print(src)
                
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    target_url = 'https://cmangaog.com/'  # Replace with the URL of the website to scrape
    force_load_images(target_url)