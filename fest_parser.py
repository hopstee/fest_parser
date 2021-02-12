import requests
import cssutils
import json
from bs4 import BeautifulSoup

file = 'fest_parser.json'

main_url = 'https://www.fest.md'
places_route = main_url + '/ru/places'
page = requests.get(places_route)

soup = BeautifulSoup(page.content, 'html.parser')

block_items = soup.find_all('div', class_="block-item")

obj = {}
js = []

for block_item in block_items:
    
    # find img link
    img_link = block_item.find('a', 'thumb')
    if img_link.has_attr('style'):
        img_link = block_item.find('a', 'thumb')['style']
        style = cssutils.parseStyle(img_link)
        img_link = style['background-image']
        img_link = img_link.replace('url(', '').replace(')', '')
    else:
        img_link = ''
    obj["img_link"] = img_link

    # find place link
    place_link = block_item.find('a', 'title')['href']
    obj["place_link"] = place_link

    # find place name
    place_name = block_item.find('a', 'title').text
    obj["name"] = place_name

    # find place address
    place_address = block_item.find('div', 'oneline').text
    obj["address"] = place_address

    # find place type
    place_type = block_item.find('div', 'oneline ellipsis').text
    place_type = place_type.split(", ")
    obj["type"] = place_type

    obj_copy = obj.copy()
    js.append(obj_copy)

with open(file, 'w', encoding='utf-8') as f:
    json.dump(js, f, ensure_ascii=False, indent=4)
