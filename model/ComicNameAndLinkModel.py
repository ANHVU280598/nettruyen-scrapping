from dataclasses import dataclass

@dataclass
class ComicNameAndLinkModel:
    hash_id: int
    name: str
    comic_url: str

    def to_dict(self):
        return {
            "hash_id": self.hash_id,
            "name": self.name,
            "comic_url": self.comic_url,
        }