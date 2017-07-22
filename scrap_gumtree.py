import requests
import re
import json
import time
import os
from bs4 import BeautifulSoup
from random import randint

headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

category = "gumtree-flats"
starting = 1
for file in os.listdir("data"):
    if file.endswith(".json"):
        name = file 
        if category in name:
            name = name.replace(category+'-', '')
            name = name.replace('.json', '')
            starting = max(starting, int(name))

queue = []
if starting > 1: #retry
    print("Returing to starting point: " + str(starting))
    queue.append("https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/page-{0}/v1c9008l3200114p{0}".format(starting))
else: #new
    queue.append("https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/v1c9008l3200114p1")

#"http://localhost:8080/gumtree.html"
#"https://www.gumtree.pl/s-pokoje-do-wynajecia/wroclaw/page-37/v1c9000l3200114p37"
#"https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/v1c9008l3200114p1"

for index, url in enumerate(queue):
    path = 'data/' + category + "-" + str(index+starting) + ".json"
    listing = []
    print("\nVisit: {}".format(queue[index]))
    delay = randint(0, 1)
    print("Delaying for {} seconds".format(delay))
    time.sleep(delay)

    response = requests.get(queue[index], headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    after = soup.find("div", {"class": "pagination"})
    after = after.find("span", {"class": "after"})
    after = after.find("a")

    if after:
        after = gumtree_link(after.get("href"))
        queue.append(after)
        print(after)
    
    not_saved = 0
    saved = 0
    if os.path.isfile(path):
        print("Already fetched, ignoring")
    else:
        for item in soup.find_all("li", {"class": "result"}):
            id = item.get("data-criteoadid")
            item = item.find_all("div", {"class": "result-link"})
            if item:
                item = item[0]
                result = item.contents[3]
                header = result.find_all("div", {"class": "title"})[0]
                title = header.find_all("a")[0].text
                link = gumtree_link(header.find_all("a")[0].get("href"))
                image = item.contents[1].find_all("img")
                if image:
                    image = image[0].get("src")

                description = result.find_all("div", {"class": "description"})
                if description:
                    description = description[0].text

                price = result.find_all("span", {"class": "amount"})
                if price:
                    price = price[0].text
                    price = int(re.sub('[^0-9]','', price))

                #print("id: {}\ncategory: {}\ntitle: {}\nlink: {}\nimage: {}\ndescription: {}\nprice: {}\n".format(
                #    id, category, title, link, image, description, price))

                if price and price > 2500:
                    not_saved += 1
                else:
                    current = {
                        'id': id, 
                        'title': title,
                        'category': category,
                        'short_description': description,
                        'link': link,
                        'image': image,
                        'price': price
                    }
                    listing.append(current)
                    saved += 1
        print("saved: {}\nnot saved: {}".format(saved, not_saved))

        with open(path, 'w') as outfile:
            json.dump(listing, outfile)

