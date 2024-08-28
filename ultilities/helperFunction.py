import hashlib
from seleniumbase import Driver
from selenium.webdriver.common.by import By
import time
import json
import os
from threading import Lock
import os
import shutil
import subprocess
from datetime import datetime
lock = Lock()


def clear_system_cache():
    # # For Linux
    # subprocess.run(['sudo', 'rm', '-rf', '/tmp/*'])
    # subprocess.run(['sudo', 'apt-get', 'clean'])

    # For macOS
    subprocess.run(['rm', '-rf', '/Library/Caches/*'])
    subprocess.run(['rm', '-rf', '~/Library/Caches/*'])
def clear_python_cache(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".pyc") or file.endswith(".pyo"):
                os.remove(os.path.join(root, file))
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))

# Clear cache in the current directory and its subdirectories
clear_python_cache(".")

def convertStrTimeToSec(date_string):
    date_format = "%d/%m/%Y %H:%M"
    date_object = datetime.strptime(date_string, date_format)

    # Convert the datetime object to seconds since the Unix epoch
    seconds_since_epoch = int(date_object.timestamp())

    return seconds_since_epoch

def conver_comicName_to_hash(name):
    # Create a hash object
    hash_object = hashlib.md5(name.encode())
    
    # Get the hexadecimal representation of the hash
    hash_id = hash_object.hexdigest()
    
    return hash_id

def scroll_to_end_of_the_page(driver):
    total_height = driver.execute_script("return document.body.scrollHeight")
    scroll_increment = total_height / 5
    for i in range(5):
        driver.execute_script(f"window.scrollTo(0, {scroll_increment * (i + 1)});")
        time.sleep(2)

def read_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_to_json(new_data, file_path='comic_chapter_data.json'):
    with lock:
        # Ensure new_data is a list of dictionaries
        if not isinstance(new_data, list):
            new_data = [new_data]
        
        # Read the existing data
        existing_data = read_json_file(file_path)
        
        # Check if existing_data is a list
        if not isinstance(existing_data, list):
            existing_data = []
        
        # Create a dictionary for easy access by hash_id
        existing_data_dict = {item['hash_id']: item for item in existing_data}

        # Update or add new data
        for item in new_data:
            if isinstance(item, dict):  # Ensure item is a dictionary
                hash_id = item.get('hash_id')
                if hash_id:
                    existing_data_dict[hash_id] = item
        
        # Convert back to list format
        updated_data = list(existing_data_dict.values())
        
        # Save the updated JSON to the file
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(updated_data, json_file, ensure_ascii=False, indent=4)