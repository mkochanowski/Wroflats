import requests
import re
import time
from bs4 import BeautifulSoup

def visit(url): 
    headers = requests.utils.default_headers()
    headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    })
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

class ListingItem:
    def __init__(self, listing_id, category, title, description, image="",price=""):
        self.hash = "NONE"
        self.category = category
        self.listing_id = listing_id
        self.title = title
        self.price = price
        self.description = description
        self.image = image


queue = ["https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/wroclaw/v1c9008l3200114p1", "https://www.gumtree.pl/s-pokoje-do-wynajecia/wroclaw/v1c9000l3200114p1"]
#url = "http://localhost:8080/gumtree.html"

for index, url in enumerate(queue):
    print("SOUP Visit: {}".format(queue[index]))
    delay = 3
    print("Delaying for {} seconds".format(delay))
    time.sleep(delay)

    soup = visit(queue[index])
    after = soup.find("div", {"class": "pagination"})
    after = after.find("span", {"class": "after"})
    after = after.find("a")

    if after:
        after = gumtree_link(after.get("href"))
        print(after)
    
    for item in soup.find_all("li", {"class": "result"}):
        print(item)
        category = "gumtree-rooms"
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
                print("--- DON'T SAVE")
            else:
                print("+++ SAVE")