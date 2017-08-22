import requests
import re
import json
import time
import os
import config
from bs4 import BeautifulSoup
from random import randint
from string import whitespace

connection = config.connect()

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

queue = ['https://www.olx.pl/nieruchomosci/stancje-pokoje/wroclaw/?search%5Bfilter_float_price%3Ato%5D=700&search%5Bfilter_enum_furniture%5D%5B0%5D=yes&search%5Bfilter_enum_roomsize%5D%5B0%5D=one']

for index, url in enumerate(queue):
    listing = []
    delay = randint(1, 3)
    print("Delaying for {} seconds".format(delay))
    time.sleep(delay)

    print("\nVisit: {}".format(queue[index]))
    response = requests.get(queue[index], headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    soup = soup.find("div", {"class": "listHandler"})
    after = soup.find("div", {"class": "pager"})
    #after = after.find("span", {"class": "fleft"})
    #after = after.find("a")

    not_saved = 0
    saved = 0
    category = 'olx-rooms'

    for item in soup.find_all("tr", {"class": "wrap"}):
        
        id = item.find("table")
        id = id.get("data-id")
        item = item.find("tbody")
        #print("\nID: {}\n{}\n\n".format(id, item))
        if item:
            with connection.cursor() as cursor:
                sql = "SELECT `id` FROM `wroflats_submissions` WHERE `item_id`=%s AND `category`=%s"
                cursor.execute(sql, (id, category))
                result = cursor.fetchone()

                if result:
                    print("item {} found, skipping".format(id))
                else:
                    header = item.find("a", {"class": "marginright5"})
                    title = header.find("strong").text
                    link = header.get("href")
                    image = item.find_all("img")
                    if image:
                        image = image[0].get("src")
                    else:
                        image = ""

                    description = item.find_all("small", {"class": "breadcrumb x-normal"})[1]
                    if description:
                        description = description.text
                        description = description.translate(dict.fromkeys(map(ord, whitespace)))
                    price = item.find("p", {"class": "price"})
                    if price:
                        price = price.text
                        price = int(re.sub('[^0-9]','', price))
                    else:
                        price = 0

                    date = item.find("p", {"class": "color-9 lheight16 marginbott5 x-normal"})
                    date = date.text
                    date = date.translate(dict.fromkeys(map(ord, whitespace)))
                    print("id: {}\ncategory: {}\ntitle: {}\nlink: {}\nimage: {}\ndescription: {}\nprice: {}\ndate: {}\n".format(id, category, title, link, image, description, price, date))

                    if price and price > 2500:
                        not_saved += 1
                    else:
                        if 'dzisiaj' in date or 'wczoraj' in date:
                            hash_id = config.rand_str(10)
                            sql = "INSERT INTO `wroflats_submissions` (`hash`, `item_id`, `category`, `title`, `short_desc`,  `thumbnail`, `link`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (hash_id, id, category, title, description, image, link, price))
                            connection.commit()
                            print("insert {}, {}".format(hash_id, title))
                            saved += 1
    print("category: " + category)
    print("saved: {}, not saved: {}".format(saved, not_saved))
    if saved > 0:
        if after:
            after = gumtree_link(after.get("href"))
            queue.append(after)
            print(after)

connection.close()