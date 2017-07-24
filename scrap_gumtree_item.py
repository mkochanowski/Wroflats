import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup
from random import randint
from string import whitespace

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

url = "https://www.gumtree.pl/a-mieszkania-i-domy-do-wynajecia/wroclaw/2pok-%2B-osobna-kuchnia-centrum-tramwaj-ul-krzywoustego-nowe-osiedle/1002042593450911217920709"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

soup = soup.find("div", {"itemtype": "http://schema.org/Product"})
gps = soup.find("span", {"class": "google-maps-link"}).get("data-uri")
gps = gps[31:] 
cords = gps.split(",")
attributes = soup.find_all("div", {"class": "attribute"})
description = soup.find("div", {"class": "description"}).text
print(description)

print("x {}, y {}".format(cords[0], cords[1]))

for atr in attributes:
    name = atr.find("span", {"class": "name"})
    value = atr.find("span", {"class": "value"})
    if name:
        name = name.text
    if value:
        value = value.text
    value = value.translate(dict.fromkeys(map(ord, whitespace)))
    print("{}: {}".format(name,value))