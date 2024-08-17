from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class Chapter:
    no_chapter: int
    chapter_title: str
    chapter_img: List[str]
    updated_at: str
    
@dataclass
class ComicChapters:
    hash_id: int    
    chapters: List[Chapter]

    def to_dict(self):
        return {
            "hash_id": self.hash_id,
            "chapters": [chapter.__dict__ for chapter in self.chapters]
        }