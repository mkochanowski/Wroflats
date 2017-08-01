import config
import datetime

connection = config.connect()

with connection.cursor() as cursor:
    #sql = "SELECT * FROM `wroflats_submissions` WHERE `id`=2429" #debug
    sql = "SELECT * FROM `wroflats_submissions` WHERE `deactivated`=0 AND `full_scrap`=1 ORDER BY `rating_date` LIMIT 500"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    
    index = 0
    for item in result:
        index += 1
        print("{}. id: {}, current rating: {} ".format(index, item['id'], item['rating']))

        # 10 points:
        # 2 - pictures
        # 3 - submission date
        # 3 - short distance 
        # 2 - price to m2

        pictures = 1
        submission_date = 10
        distance = 60
        price_to_m2 = 0

        # pictures
        if item['pictures']:
            pictures = len(item['pictures'])
            pictures = min(pictures, 800)
        pictures = (pictures / 800)*2
        pictures = round(pictures, 3)

        # submission date
        if item['submission_date']:
            # item['submission_date'] = datetime.date(2017, 7, 15)
            added = datetime.datetime.combine(item['submission_date'], datetime.time.min)
            now = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
            subtract = now - added
            print(subtract)
            submission_date = subtract.days
        submission_date = 3/(1+submission_date*0.25)
        submission_date = round(submission_date, 3)

        # distance
        if item['distance_time']:
            if (item['distance_transit'] == 0) or (item['distance_transit'] == 1591) or ('godz' in item['distance_time']):
                distance = 60
            else:
                distance = int(item['distance_time'][:-4])
            # print("{}, {}".format(item['distance_transit'], item['distance_time']))
        distance = (61-distance)/20
        distance = round(distance, 3)
        # print(distance)

        # price 
        if item['m2'] and item['price'] and (int(item['price']) > 0) and (int(item['m2']) > 0):
            item['m2'] = min(100, int(item['m2']))
            price_to_m2 = item['price']/item['m2']
            price_to_m2 = (61-price_to_m2)/20
            if price_to_m2 < 0:
                price_to_m2 = 0
        price_to_m2 = round(price_to_m2, 3)
            #print("price: {}; m2: {}".format(item['price'], item['m2']))
        #print(price_to_m2)

        # final rating
        final_rating = pictures + submission_date + distance + price_to_m2
        final_rating *= item['rating_modifier']
        final_rating = round(final_rating, 3)
        final_rating = max(0, final_rating) # check if <0
        final_rating = min(10, final_rating) # check if >10
        print("pictures: {}\nsubmission date: {}\ndistance: {}\nprice to m2: {}\nrating modifier: {}\nfinal rating: {}".format(pictures, submission_date, distance, price_to_m2, item['rating_modifier'], final_rating))
    
        with connection.cursor() as cursor:
            sql = "UPDATE `wroflats_submissions` SET `rating`=%s, `rating_date`=%s WHERE `id`=%s"
            f = '%Y-%m-%d %H:%M:%S'
            rating_date = datetime.datetime.now().strftime(f)
            cursor.execute(sql, (final_rating, rating_date, item['id']))
            connection.commit()
            cursor.close()
            print("Ranking updated\n")

connection.close()