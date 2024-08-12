from dataclasses import dataclass
from typing import List

@dataclass
class ComicName:
    hash_id: int
    comic_name: str
    comic_url: str
    source: str

    def to_dict(self):
        return {
            "hash_id": self.hash_id,
            "comic_name": self.comic_name,
            "comic_url": self.comic_url,
            "source" : self.source
        }
