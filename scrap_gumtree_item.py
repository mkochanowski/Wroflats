import requests
import re
import json
import time
import os
import config
import datetime
from bs4 import BeautifulSoup
from random import randint
from string import whitespace

connection = config.connection
env = config.os.environ
headers = requests.utils.default_headers()
headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
})

def gumtree_link(link):
    if "http" not in link:
        link = "https://www.gumtree.pl" + link
    return link

to_update = []
cords_out = []
with connection.cursor() as cursor:
    sql = "SELECT `id`, `link` FROM `wroflats_submissions` WHERE `full_scrap`=0 LIMIT 25"
    cursor.execute(sql)
    result = cursor.fetchall()

    if result:
        for item in result:
            delay = randint(0, 2)
            print("Delaying for {} seconds".format(delay))
            time.sleep(delay)

            print('id: {} link: {}'.format(item['id'], item['link']))

            url = item['link']

            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, "html.parser")

            soup = soup.find("div", {"itemtype": "http://schema.org/Product"})
            gps = soup.find("span", {"class": "google-maps-link"})
            
            if gps:
                gps = gps.get("data-uri")
                gps = gps[31:] 
            else:
                gps = '0,0'
            
            cords = gps.split(",")
            attributes = soup.find_all("div", {"class": "attribute"})
            description = soup.find("div", {"class": "description"})
            if description:
                description = description.text
            pictures = soup.find("script", {"id": "vip-gallery-data"})
            
            if pictures: 
                #print(pictures.text)
                pictures = json.loads(pictures.text, strict=False)
                if pictures['large']:
                    pictures = pictures['large']
                elif pictures['medium']:
                    pictures = pictures['medium']
                elif pictures['small']:
                    pictures = pictures['small']
            else:
                pictures = ""

            #print(description)

            #print("x {}, y {}".format(cords[0], cords[1]))
            attribute_out = []
            m2 = ""
            baths = ""
            rooms = ""
            ts = '2013-01-12 15:27:43'
            f = '%Y-%m-%d %H:%M:%S'
            scrap_date = datetime.datetime.now().strftime(f)
            submission_date = '0000-00-00'
            available_date = '0000-00-00'
            for atr in attributes:
                name = atr.find("span", {"class": "name"})
                value = atr.find("span", {"class": "value"})
                if name:
                    name = name.text
                if value:
                    value = value.text
                value = value.translate(dict.fromkeys(map(ord, whitespace)))
                attribute_out.append({name: value})

                fg = '%d/%m/%Y'
                if 'Data dodania' in name:
                    submission_date = datetime.datetime.strptime(value, fg).strftime('%Y-%m-%d')
                elif 'Dostępny' in name:
                    available_date = datetime.datetime.strptime(value, fg).strftime('%Y-%m-%d')
                elif 'pokoi' in name:
                    rooms = value
                elif 'łazienek' in name:
                    baths = value
                elif 'Wielkość (m2)' in name:
                    m2 = value
            #    print("{}: {}".format(name,value))
            #print(attribute_out)
            #print(pictures)

            to_update.append({
                'id': item['id'],
                'full_desc': description,
                'submission_date': submission_date,
                'available_date': available_date,
                'm2': m2,
                'rooms': rooms,
                'baths': baths,
                'cord_x': cords[0],
                'cord_y': cords[1],
                'pictures': pictures,
                'attributes': attribute_out,
                'full_scrap': 1,
                'scrap_date': scrap_date,
                'distance_transit': 0,
                'distance_time': ''
            })
            cords_out.append({'x': cords[0], 'y': cords[1]})

    #print(cords_out)
    print("51.111039,17.053092")
    origins = ""
    origins_set = True
    for item in cords_out:
        if origins_set:
            origins += "|"
        origins += "{},{}".format(item['x'], item['y'])

    payload = {'language': 'pl-PL', 'mode': 'transit', 'origins': origins, 'destinations': '51.111039,17.053092', 'key': env['GMAPS'], 'arrival_time': '1501657200'}
    gmaps = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json", params=payload)
    print("Gmaps url: " + gmaps.url)
    dist = json.loads(gmaps.text)
    #print(dist)
    index = 0
    for item in dist['rows']:
        item = item['elements'][0]
        if item['status'] == 'OK':
            #print(item['duration']['text'])
            #print(item['distance']['value'])
           
            to_update[index]['distance_transit'] = item['distance']['value']
            to_update[index]['distance_time'] = item['duration']['text']
        index += 1

for item in to_update:
    values = []
    up_id = item['id']
    data = ""
    for i in item:
        if i != 'id':
            data += "`{}`=%s, ".format(i)
            values.append(str(item[i]))

    #print(values)
    up_query = "UPDATE `wroflats_submissions` SET {} WHERE `id`='{}'".format(data[:-2], up_id)
    #print(up_query)

    with connection.cursor() as cursor:
        cursor.execute(up_query, (values))
        connection.commit()
    
print("Updated")