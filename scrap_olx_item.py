import requests
import re
import json
import time
import os
import config
import datetime
import logging
import sys
import browser
from bs4 import BeautifulSoup
from random import randint
from string import whitespace
from urllib.parse import urlparse, parse_qs

connection = config.connect()
env = config.os.environ
headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})
logging.basicConfig(level=logging.ERROR, filename='logs-olx_item.log')

to_update = []
cords_out = []
with connection.cursor() as cursor:
    sql = "SELECT `id`, `link`, `full_scrap`, `distance_transit`, `distance_walking`, `distance_time` FROM `wroflats_submissions` WHERE `deactivated`=0 AND `category` LIKE '%olx%' ORDER BY `scrap_date` LIMIT 5"
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        driver = browser.driver()
        for item in result:
            delay = randint(0, 2)
            print("Delaying for {} seconds".format(delay))
            #time.sleep(delay)

            print('id: {} link: {}'.format(item['id'], item['link']))
            url = item['link']

            try:
                driver.get(url)
                element = driver.find_element_by_id("showMap").click()
                time.sleep(2)
                soup = driver.page_source
                soup = BeautifulSoup(soup, "html.parser")
                soup = soup.find("div", {"id": "googlemap"})
                link = soup.find("a").get("href")
                print(link)
                o = urlparse(link)
                query = parse_qs(o.query)
                gps = query['ll'][0]
                print('CORDS: {}\n'.format(gps))
                cords = gps.split(",")
                print(cords)
                f = '%Y-%m-%d %H:%M:%S'
                scrap_date = datetime.datetime.now().strftime(f)
                if item['full_scrap'] == 0:
                    to_update.append({
                        'id': item['id'],
                        'cord_x': cords[0],
                        'cord_y': cords[1],
                        'full_scrap': 1,
                        'scrap_date': scrap_date
                    })
                else:
                    print("full scrap done, skipping")

            except Exception as e:
                print("Exception caught, skipping")
                logging.exception(url)
                
        driver.close()
 
for item in to_update:
    values = []
    up_id = item['id']
    data = ""
    for i in item:
        if i != 'id':
            data += "`{}`=%s, ".format(i)
            values.append(str(item[i]))

    # print(values)
    up_query = "UPDATE `wroflats_submissions` SET {} WHERE `id`='{}'".format(data[:-2], up_id)
    # print(up_query)

    with connection.cursor() as cursor:
        cursor.execute(up_query, (values))
        connection.commit()
    
print("Updated")

connection.close()