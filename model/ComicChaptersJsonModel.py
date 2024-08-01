from dataclasses import dataclass
from typing import List

@dataclass
class Chapter:
    number: int
    img_source: List[str]

@dataclass
class ComicChapterModel:
    id: int
    img_src: str
    name: str
    different_name: str
    author: str
    status: str
    kinds: List[str]
    view_count: int
    chapters: List[Chapter]

    def to_dict(self):
        return {
            "id": self.id,
            "img_src": self.img_src,
            "name": self.name,
            "different_name": self.different_name,
            "author": self.author,
            "status": self.status,
            "kinds": self.kinds,
            "view_count": self.view_count,
            "chapters": [chapter.__dict__ for chapter in self.chapters]
        }