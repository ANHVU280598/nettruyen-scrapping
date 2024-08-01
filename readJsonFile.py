import json

# Define a dataclass to store the link_source
from dataclasses import dataclass
from typing import List

@dataclass
class comicShort:
    id: str
    comic_url: str

def read_json_file(file_path: str) -> List[comicShort]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    comics_info = []
    
    for item in data:
        comic_short = comicShort(
            id=item.get('id', ''),
            comic_url=item.get('comic_url', '')
        )
        comics_info.append(comic_short)

    return comics_info
