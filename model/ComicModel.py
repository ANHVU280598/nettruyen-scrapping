from dataclasses import dataclass
from typing import List
from datetime import datetime

@dataclass
class Chapter:
    no_chapter: int
    chapter_title: str
    chapter_img: List[str]
    updated_at: datetime

@dataclass
class ComicGeneral:
    id: int
    comic_name: str
    hash_id: int
    other_name: str
    author_name: str
    status: str
    kinds: List[str]
    img_src: str
    comic_url: str
    view_count: int
    comment: int
    rating: int
    newest_chapter: str
    # updated_at: int
    chapters: List[Chapter]

    def to_dict(self):
        return {
            "id": self.id,
            "comic_name": self.comic_name,
            "hash_id": self.hash_id,
            "other_name": self.other_name,
            "img_src": self.img_src,
            "author_name": self.author_name,
            "status": self.status,
            "kinds": self.kinds,
            "comic_url": self.comic_url,
            "view_count": self.view_count,
            "comment": self.comment,
            "rating": self.rating,
            "newest_chapter": self.newest_chapter,
            # "updated_at": self.updated_at,
            "chapters": [chapter.__dict__ for chapter in self.chapters]
        }
