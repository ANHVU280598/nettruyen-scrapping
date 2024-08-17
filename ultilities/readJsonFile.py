import json

# Define a dataclass to store the link_source
from dataclasses import dataclass
from typing import List

@dataclass
class comicShort:
    hash_id: str
    comic_url: str
    comic_name: str

def read_json_file(file_path: str) -> List[comicShort]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    comics_info = []
    
    for item in data:
        comic_short = comicShort(
            hash_id=item.get('hash_id', ''),
            comic_url=item.get('comic_url', ''),
            comic_name = item.get('comic_name','')
        )
        comics_info.append(comic_short)

    return comics_info
