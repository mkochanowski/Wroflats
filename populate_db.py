import os
import json
import random, string
import config

connection = config.connection

def rand_str(length):
    return ''.join(
        random.choice(string.ascii_uppercase) for i in range(length))

'''
['hash_id', 'item_id', 'category', 'title', 'short_desc', 'full_description', 'thumb_image', 'link', 'price', 'submission_date', 'available_date', 'm2', 'rooms', 'bath', 'gps_link', 'distance', 'scrap_date', 'full_scrap', 'rate', 'favorite', 'comment']
'''

full_desc = ""
submission_date = ""
available_date = ""
m2 = ""
rooms = ""
bath = ""
cord_x = 0
cord_y = 0
distance = 0
scrap_date = ""
full_scrap = 0
rating = 0
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
                with connection.cursor() as cursor:
                    sql = "SELECT `id` FROM `wroflats_submissions` WHERE `item_id`=%s AND `category`=%s"
                    cursor.execute(sql, (item['id'], item['category']))
                    result = cursor.fetchone()

                    if result:
                        print("item {} found, skipping".format(item['id']))
                    else:
                        hash_id = rand_str(10)
                        # print(hash_id)
                        item_id = item['id']
                        category = item['category']
                        title = item['title']
                        short_desc = item['short_description']
                        price = item['price']
                        if not item['price']:
                            price = 0
                        link = item['link']
                        thumb_image = item['image']
                        if not thumb_image:
                            thumb_image = ""
                        '''to_add = [ 
                            hash_id, item_id, category, title, short_desc, full_description, thumb_image, link, price, submission_date, available_date, m2, rooms, bath, gps_link, distance, scrap_date, full_scrap, rating, favorite, comment
                        ]'''
                        with connection.cursor() as cursor:
                            # Create a new record
                            sql = "INSERT INTO `wroflats_submissions` (`hash`, `item_id`, `category`, `title`, `short_desc`, `full_desc`, `thumbnail`, `link`, `price`, `submission_date`, `available_date`, `m2`, `rooms`, `baths`, `cord_x`, `cord_y`, `distance`, `scrap_date`, `full_scrap`, `rating`, `favorite`, `comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(sql, (hash_id, item_id, category, title, short_desc, full_desc, thumb_image, link, price, submission_date, available_date, m2, rooms, bath, cord_x, cord_y, distance, scrap_date, full_scrap, rating, favorite, comment))
                            connection.commit()
                            print("insert {}, {}".format(hash_id, title))
                
        os.rename(path, path + '.done')
