import gspread
import os
import json
import random, string

def rand_str(length):
    return ''.join(
        random.choice(string.ascii_uppercase) for i in range(length))

full_description = ""
submission_date = ""
available_date = ""
m2 = 0
rooms = ""
bath = ""
gps_link = ""
distance = ""
scrap_date = ""
full_scrap = 0
rate = 0
favorite = 0
comment = ""

output = []
output_path = 'gumtree-full.json'
working = []
index = 0
location = 0
for file in os.listdir("data"):
    if file.endswith(".json"): 
        path = os.path.join('data', file)
        index += 1
        print("{} - {}".format(index, path))
        with open(path, 'r') as outfile:
            working = json.load(outfile)

            for item in working:
                location += 1    
                hash_id = rand_str(20)
                print("  " + hash_id)
                item_id = item['id']
                category = item['category']
                title = item['title']
                short_desc = item['short_description']
                price = item['price']
                if not item['price']:
                    price = 0
                link = item['link']
                thumb_image = item['image']
                
                to_add = {
                    'hash_id': hash_id, 
                    'item_id': item_id, 
                    'category': category, 
                    'title': title, 
                    'short_desc': short_desc, 
                    'full_description': full_description, 
                    'thumb_image': thumb_image, 
                    'link': link, 
                    'price': price, 
                    'submission_date': submission_date, 
                    'available_date': available_date, 
                    'm2': m2, 
                    'rooms': rooms, 
                    'bath': bath, 
                    'gps_link': gps_link, 
                    'distance': distance, 
                    'scrap_date': scrap_date, 
                    'full_scrap': full_scrap, 
                    'rate': rate, 
                    'favorite': favorite, 
                    'comment': comment
                }
                output.append(to_add)
                #worksheet.append_row(to_add)
                
        #os.rename(path, path + '.done')
print("Files: {}, locations: {}".format(index, location))
with open(output_path, 'w') as outfile:
    json.dump(output, outfile)