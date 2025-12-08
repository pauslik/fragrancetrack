import os
import re
from curl_cffi import requests
from bs4 import BeautifulSoup


def write_temp_html(html):
    with open(os.path.abspath("./temp.html"), "w") as file:
        file.write(html)

# TODO see if it's possible to only get the meta tages in head instead of the whole page
def get_fragrantica_html(link):
    response = requests.get(link, impersonate="chrome")
    if response.status_code == 200:
        html = response.text
        write_temp_html(html)
    else:
        raise Exception(f"Failed to get the HTML: {response.status_code}:{response.text}")

    return html

def parse_fragrantica_page(html: str) -> dict:
    result = {}
    card_repository = "https://fimgs.net/mdimg/perfume-social-cards/"
    pattern = r'[^/]+$'

    soup = BeautifulSoup(html, 'html.parser')

    image_link = None
    all_images = soup.find_all("meta", property="og:image")
    for image in all_images:
        link = image["content"]
        if isinstance(link, str):
            if link.startswith(card_repository+'en-p_c'):
                image_link = link
                break

    if image_link == None:
        raise Exception(f'Link to card not found')

    match = re.search(pattern, image_link)
    if isinstance(match, re.Match):
        image_file = match.group(0)
    else:
        raise Exception(f'Card link pattern ({pattern}) not found in string: {image_link}')
    card_link = card_repository + image_file
    
    # returning a dict just in case we would want to parse for something more
    result["card"] = card_link

    return result

def download_fragrantica_card(frag_link, file_path, overwrite=True):
    if os.path.exists(file_path) and not overwrite:
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
