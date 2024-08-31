import json

if __name__ == "__main__":
    file_path_comic_name = 'comic_name.json'
    file_path_comic_chapter = 'comic_chapters.json'

    comic_name_data = []
    comic_chapter_data = []

    with open(file_path_comic_name, 'r') as file:
        comic_name_data = json.load(file)

    with open(file_path_comic_chapter, 'r') as file:
        comic_chapter_data = json.load(file)

    print(len(comic_name_data))

    print(comic_chapter_data[282])