from bs4 import BeautifulSoup
import requests
from model.manga_title import MangaTitle
from misc.constants import page
from misc.methods import download, create_catalog, get_list_of_images


def detect_new(site, expected_titles):
    generated_html = requests.get(f'{site}')

    page_parsed = BeautifulSoup(generated_html.text, 'html.parser')
    page_object = page_parsed.find_all("a", "text-white text-lg font-bold")

    links = [page_object[i]['href'] for i in range(len(page_object))]
    titles = [page_object[i].text for i in range(len(page_object))]

    for expected in expected_titles:
        for title in titles:
            if expected in title:

                current_title = MangaTitle(title)

                if current_title.is_the_latest():
                    path = create_catalog(title)
                    images = get_list_of_images(titles, links, title, site)
                    download(images, title, path)




while True:
    detect_new(page, ["Jujutsu Kaisen", "One Piece"])
