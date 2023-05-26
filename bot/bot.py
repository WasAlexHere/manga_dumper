from bs4 import BeautifulSoup
import requests
import os
import shutil
from model.manga_title import MangaTitle

page = 'https://onepiecechapters.com'


def detect_new(site):
    generated_html = requests.get(f'{page}')

    page_parsed = BeautifulSoup(generated_html.text, 'html.parser')
    page_object = page_parsed.find_all("a", "text-white text-lg font-bold")

    links = []
    titles = []

    for i in range(len(page_object)):
        links.append(page_object[i]['href'])
        titles.append(page_object[i].text)

    for title in titles:
        if 'One Piece' in title:
            current_title = MangaTitle(title)
            current_title.check_for_latest()

            path = os.path.join(os.getcwd(), title)

            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)

            title_id = titles.index(title)
            new_page = f'{page}{links[title_id]}'
            new_html = requests.get(new_page)
            parsed_page = BeautifulSoup(new_html.text, 'html.parser')
            images = parsed_page.find_all("img", class_="fixed-ratio-content")

            download(images, title, path)


def download(files, title, path):
    for image in files:
        link = image['src']
        filename = link.split('/')[-1]
        get_image = requests.get(link)
        open(os.path.join(path, filename), 'wb').write(get_image.content)
        print(f'DONE ::: {filename} :::')
    print(f'\n::: {title} is downloaded:::\n')
    shutil.make_archive(title, 'zip', title)
    arch_name = title + '.zip'
    arch_path = os.path.join(os.getcwd(), arch_name)
    shutil.rmtree(path)


detect_new(page)

