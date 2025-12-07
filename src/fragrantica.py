import os
import re
from curl_cffi import requests
from bs4 import BeautifulSoup


def write_temp_html(html):
    with open(os.path.abspath("./temp.html"), "w") as file:
        file.write(html)

# def find_fragrantica_page(frag: Fragrance):
#     link = frag.link
#     # link = "https://www.fragrantica.com/perfume/Amouage/Reflection-Man-920.html"
#     return link

def get_fragrantica_html(link):
    response = requests.get(link, impersonate="chrome")
    if response.status_code == 200:
        html = response.text
        # write_temp_html(html)
    else:
        raise Exception(f"Failed to get the HTML: {response.status_code}:{response.text}")

    return html

def parse_fragrantica_page(html: str) -> dict:
    result = {}
    card_repository = "https://fimgs.net/mdimg/perfume-social-cards/"
    pattern = r'[^/]+$'

    soup = BeautifulSoup(html, 'html.parser')

    # find card link (expect this to be in the same place everytime)
    # image_container = soup.find("div", class_="carousel-cell-photo is-selected")
    # print(image_container)
    # image = image_container.find("div").find("a")
    # image_link = image["href"]


    all_images = soup.find_all("meta", property="og:image")
    for image in all_images:
        link = image["content"]
        if isinstance(link, str):
            if link.startswith(card_repository+'en-p_c'):
                image_link = link
                break
    # TODO add an exception after it checks every meta tag and doesn't find the correct one
    match = re.search(pattern, image_link)
    if isinstance(match, re.Match):
        image_file = match.group(0)
    else:
        raise Exception(f'Card link pattern ({pattern}) not found in string: {image_link}')
    card_link = card_repository + image_file
    
    result["card"] = card_link

    # TODO parse all other info
    # return aggregated dict with all relevant values found
    return result

def download_fragrantica_card(frag_link, file_path):
    # TODO check if the image already exists
    if os.path.exists(file_path):
        return False
    frag_html = get_fragrantica_html(frag_link)
    html_dict = parse_fragrantica_page(frag_html)
    card_link = html_dict["card"]

    response = requests.get(card_link, impersonate="chrome")
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")
