from dataclasses import dataclass
from typing import List

@dataclass
class ComicGeneral:
    id: int
    name: str
    img_src: str
    comic_url: str
    view_count: int
    comment: int
    love: int
    newest_chapter: str
    updated_at: int

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "img_src": self.img_src,
            "comic_url": self.comic_url,
            "view_count": self.view_count,
            "comment": self.comment,
            "love": self.love,
            "newest_chapter": self.newest_chapter,
            "updated_at": self.updated_at,
        }