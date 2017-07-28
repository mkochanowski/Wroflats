import requests
import re
import json
import time
import os
import config
from bs4 import BeautifulSoup
from random import randint
from string import whitespace

connection = config.connection

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

with connection.cursor() as cursor:
    sql = "SELECT `id`, `link` FROM `wroflats_submissions` WHERE `full_scrap`=0 LIMIT 1"
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        for item in result:
            print('id: {} link: {}'.format(item['id'], item['link']))

            url = item['link']

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            soup = soup.find("div", {"itemtype": "http://schema.org/Product"})
            gps = soup.find("span", {"class": "google-maps-link"}).get("data-uri")
            gps = gps[31:] 
            cords = gps.split(",")
            attributes = soup.find_all("div", {"class": "attribute"})
            description = soup.find("div", {"class": "description"}).text
            pictures = soup.find("script", {"id": "vip-gallery-data"}).text
            if pictures: 
                pictures = json.loads(pictures)
                if pictures['large']:
                    pictures = pictures['large']
                elif pictures['medium']:
                    pictures = pictures['medium']
                elif pictures['small']:
                    pictures = pictures['small']
            else:
                pictures = ""

            print(description)

            print("x {}, y {}".format(cords[0], cords[1]))
            attribute = []
            for atr in attributes:
                name = atr.find("span", {"class": "name"})
                value = atr.find("span", {"class": "value"})
                if name:
                    name = name.text
                if value:
                    value = value.text
                value = value.translate(dict.fromkeys(map(ord, whitespace)))
                attribute.append({name: value})
                print("{}: {}".format(name,value))
            print(attribute)
            print(pictures)
