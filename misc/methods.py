import requests
import shutil
import os
from bs4 import BeautifulSoup


def download(files, title, path):
    for image in files:
        link = image['src']
        filename = link.split('/')[-1]
        get_image = requests.get(link)
        open(os.path.join(path, filename), 'wb').write(get_image.content)
        print(f'DONE ::: {filename} :::')
    print(f'\n::: {title} is downloaded:::\n')
    # shutil.make_archive(title, 'zip', title)
    # shutil.rmtree(path)


def create_catalog(title):
    path = os.path.join(os.getcwd(), title)

    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

    return path


def get_list_of_images(titles, links, title, site):
    title_id = titles.index(title)
    new_page = f'{site}{links[title_id]}'
    new_html = requests.get(new_page)
    parsed_page = BeautifulSoup(new_html.text, 'html.parser')
    images = parsed_page.find_all("img", class_="fixed-ratio-content")

    return images
