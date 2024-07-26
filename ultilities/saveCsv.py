import csv
import os

def write_comic_to_csv(comic, csv_file='ComicGeneral.csv'):
    # Check if the file exists to write headers only once
    write_header = not os.path.exists(csv_file)

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header if file does not exist
        if write_header:
            writer.writerow(["ID", "Name", "Image Source", "Comic URL", "View Count", "Comment", "Love", "Newest Chapter", "Updated At"])

        # Write comic data
        writer.writerow([
            comic.id,
            comic.name,
            comic.img_src,
            comic.comic_url,
            comic.view_count,
            comic.comment,
            comic.love,
            comic.newest_chapter,
            comic.updated_at
        ])