import requests
import re
import json
import time
import os
import config
from bs4 import BeautifulSoup
from random import randint

connection = config.connection

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

queue = ['https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/v1c9008l3200114p1?sort=dt&order=desc', 'https://www.gumtree.pl/s-pokoje-do-wynajecia/wroclaw/v1c9000l3200114p1?sort=dt&order=desc']
'''
starting = 1
for file in os.listdir("data"):
    if file.endswith(".json"):
        name = file 
        if category in name:
            name = name.replace(category+'-', '')
            name = name.replace('.json', '')
            starting = max(starting, int(name))

if starting > 1: #retry
    print("Returing to starting point: " + str(starting))
    queue.append("https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/page-{0}/v1c9008l3200114p{0}".format(starting))
else: 
    queue.append("https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/v1c9008l3200114p1")
'''

for index, url in enumerate(queue):
#   path = 'data/' + category + "-" + str(index+starting) + ".json"
    listing = []
    delay = randint(1, 3)
    print("Delaying for {} seconds".format(delay))
    time.sleep(delay)

    print("\nVisit: {}".format(queue[index]))
    response = requests.get(queue[index], headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    after = soup.find("div", {"class": "pagination"})
    after = after.find("span", {"class": "after"})
    after = after.find("a")
    
    not_saved = 0
    saved = 0
    for item in soup.find_all("li", {"class": "result"}):
        id = item.get("data-criteoadid")
        item = item.find_all("div", {"class": "result-link"})
        if item:
            if "s-pokoje-do-wynajecia" in url:
                category = 'gumtree-rooms'
            elif "s-mieszkania-i-domy-do-wynajecia" in url:
                category = 'gumtree-flats'
            else:
                category = 'unknown'

            with connection.cursor() as cursor:
                sql = "SELECT `id` FROM `wroflats_submissions` WHERE `item_id`=%s AND `category`=%s"
                cursor.execute(sql, (id, category))
                result = cursor.fetchone()

                if result:
                    print("item {} found, skipping".format(id))
                else:
                    item = item[0]
                    result = item.contents[3]
                    header = result.find_all("div", {"class": "title"})[0]
                    title = header.find_all("a")[0].text
                    link = gumtree_link(header.find_all("a")[0].get("href"))
                    image = item.contents[1].find_all("img")
                    if image:
                        image = image[0].get("src")
                    else:
                        image = ""

                    description = result.find_all("div", {"class": "description"})
                    if description:
                        description = description[0].text

                    price = result.find_all("span", {"class": "amount"})
                    if price:
                        price = price[0].text
                        price = int(re.sub('[^0-9]','', price))
                    else:
                        price = 0

                    #print("id: {}\ncategory: {}\ntitle: {}\nlink: {}\nimage: {}\ndescription: {}\nprice: {}\n".format(id, category, title, link, image, description, price))

                    if price and price > 2500:
                        not_saved += 1
                    else:
                        hash_id = config.rand_str(10)
                        sql = "INSERT INTO `wroflats_submissions` (`hash`, `item_id`, `category`, `title`, `short_desc`,  `thumbnail`, `link`, `price`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                        cursor.execute(sql, (hash_id, id, category, title, description, image, link, price))
                        connection.commit()
                        print("insert {}, {}".format(hash_id, title))
                        saved += 1
    print("cateogory: " + category)
    print("saved: {}, not saved: {}".format(saved, not_saved))
    if saved > 0:
        if after:
            after = gumtree_link(after.get("href"))
            queue.append(after)
            print(after)

#   with open(path, 'w') as outfile:
#       json.dump(listing, outfile)

