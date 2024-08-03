import json
import base64
import requests
import os

def image_to_base64(url):
    """Convert an image URL to a base64 string."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Read the JSON data from the file
with open('comic_chapter_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Temporary file to store updated data
temp_filename = 'temp_updated_comics_data.json'

# Open the temporary file in write mode
with open(temp_filename, 'w', encoding='utf-8') as temp_file:
    temp_file.write('[')  # Start the JSON array

    for index, comic in enumerate(data):
        # Extract the necessary fields
        comic_id = comic.get('id')
        hash_id = comic.get('hash_id')
        comic_name = comic.get('comic_name')
        chapters = comic.get('chapters', [])

        # Process each chapter
        updated_chapters = []
        for chapter in chapters:
            no_chapter = chapter.get('no_chapter')
            chapter_img_urls = chapter.get('chapter_img', [])

            # Convert each image URL to Base64
            chapter_img_base64 = [image_to_base64(url) for url in chapter_img_urls]

            # Store the chapter with converted images
            updated_chapters.append({
                'no_chapter': no_chapter,
                'chapter_img': chapter_img_base64
            })

        # Store the updated comic data
        updated_comic = {
            'id': comic_id,
            'hash_id': hash_id,
            'comic_name': comic_name,
            'chapters': updated_chapters
        }

        # Write the updated comic data to the temporary file
        json.dump(updated_comic, temp_file, ensure_ascii=False, indent=4)

        # Add a comma if not the last comic
        if index < len(data) - 1:
            temp_file.write(',')

        print(f"Updated and saved comic with id: {comic_id}")

    temp_file.write(']')  # End the JSON array

# Replace the original file with the updated file
os.replace(temp_filename, 'updated_comics_data.json')