import json
import os
from threading import Lock

lock = Lock()

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