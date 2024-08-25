from dataclasses import dataclass
from typing import List

@dataclass
class ComicHomePage:
    hash_id: int
    name: str
    comic_url: str
    description: str
    no_chapter: int
    no_comment: int
    genres: List[str]
    img_url: str

    def to_dict(self):
        return {
            "hash_id": self.hash_id,
            "name": self.name,
            "comic_url": self.comic_url,
            "description": self.description,
            "no_chapter": self.no_chapter,
            "no_comment": self.no_comment,
            "genres": self.genres,
            "img_url": self.img_url
        }