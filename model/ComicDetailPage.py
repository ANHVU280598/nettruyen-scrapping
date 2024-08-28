from dataclasses import dataclass
from typing import List



@dataclass
class ComicDetailPage:
    hash_id: int
    name: str
    img_url: str
    description: str
    author: str
    genres: List[str]
    view: int
    update: str
    chapters: List[str]

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