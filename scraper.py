import requests
from bs4 import BeautifulSoup

r = requests.get("http://localhost:8080/gumtree.html")
soup = BeautifulSoup(r.content, "html.parser")

#gumtree
for item in soup.find_all("div", {"class": "result-link"}):
    result = item.contents[3]
    header = result.find_all("div", {"class": "title"})[0]
    title = header.find_all("a")[0].text
    link = header.find_all("a")[0].get("href")
    description = result.find_all("div", {"class": "description"})[0].text
    amount = result.find_all("span", {"class": "amount"})[0].text
    print("title: {} \nlink: {} \ndescription: {} \namount: {} \n".format(title, link, description, amount))

    #print("{} \n".format(result))