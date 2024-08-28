from dataclasses import dataclass
from typing import List

@dataclass
class ComicDetail:
    hash_id: int
    comic_name: str
    img_src: str
    rating: str
    view: str
    other_name: List[str]
    genres: List[str]
    status: str
    chapters: List[str]
    lastUpdate: int
    description: str
    no_chapter: int
    author: str

    def to_dict(self):
        return {
            "hash_id": self.hash_id,
            "comic_name": self.comic_name,
            "img_src": self.img_src,
            "rating": self.rating,
            "view": self.view,
            "other_name": self.other_name,
            "genres": self.genres,
            "status": self.status,
            "chapters": self.chapters,
            "lastUpdate": self.lastUpdate,
            "description": self.description,
            "no_chapter": self.no_chapter,
            "author": self.author
        }