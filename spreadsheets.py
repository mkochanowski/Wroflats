import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
import random, string

def rand_str(length):
    return ''.join(
        random.choice(string.ascii_uppercase) for i in range(length))

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', scope)

gc = gspread.authorize(credentials)

spr = gc.open_by_key('1LCE5eJdx9oy_dJloyj2VQVe7ZlE60qXEIhbTM5ihRt4')
worksheet = spr.worksheet("Locations")
#values_list = worksheet.row_values(1)

'''
['hash_id', 'item_id', 'category', 'title', 'short_desc', 'full_description', 'thumb_image', 'link', 'price', 'submission_date', 'available_date', 'm2', 'rooms', 'bath', 'gps_link', 'distance', 'scrap_date', 'full_scrap', 'rate', 'favorite', 'comment', '', '', '', '', '', '', '']
'''

full_description = ""
submission_date = ""
available_date = ""
m2 = ""
rooms = ""
bath = ""
gps_link = ""
distance = ""
scrap_date = ""
full_scrap = 0
rate = 0
favorite = 0
comment = ""

working = []
for file in os.listdir("data"):
    if file.endswith(".json"): 
        path = os.path.join('data', file)
        print(path)
        with open(path, 'r') as outfile:
            working = json.load(outfile)

            for item in working:
                hash_id = rand_str(10)
                print(hash_id)
                item_id = item['id']
                category = item['category']
                title = item['title']
                short_desc = item['short_description']
                price = item['price']
                if not item['price']:
                    price = 0
                link = item['link']
                thumb_image = item['image']
                to_add = [ 
                    hash_id, item_id, category, title, short_desc, full_description, thumb_image, link, price, submission_date, available_date, m2, rooms, bath, gps_link, distance, scrap_date, full_scrap, rate, favorite, comment
                ]
                worksheet.append_row(to_add)
                
        os.rename(path, path + '.done')
        break