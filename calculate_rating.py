import config
import datetime

connection = config.connection

with connection.cursor() as cursor:
    sql = "SELECT * FROM `wroflats_submissions` WHERE `deactivated`=0 AND `full_scrap`=1 ORDER BY `rating_date` LIMIT 100"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    
    # print(result)

    for item in result:
        print("{} {} ".format(item['id'], item['rating']))

        # 10 points:
        # 2 - pictures
        # 4 - submission date
        # 2 - short distance 
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

        # submission date
        if item['submission_date']:
            # item['submission_date'] = datetime.date(2017, 7, 15)
            added = datetime.datetime.combine(item['submission_date'], datetime.time.min)
            now = datetime.datetime.combine(datetime.datetime.now(), datetime.time.min)
            subtract = now - added
            submission_date = subtract.days
            if submission_date == 0:
                submission_date = 1
            elif submission_date:
                submission_date /= 3
        submission_date = 4/(submission_date)
        
        # distance
        if item['distance_time']:
            if (item['distance_transit'] == 0) or (item['distance_transit'] == 1591) or ('godz' in item['distance_time']):
                distance = 60
            else:
                distance = int(item['distance_time'][:-4])
            # print("{}, {}".format(item['distance_transit'], item['distance_time']))
        distance = (61-distance)/30
        # print(distance)

        # price 
        if item['m2'] and item['price'] and (int(item['price']) > 0) and (int(item['m2']) > 0):
            item['m2'] = min(100, int(item['m2']))
            price_to_m2 = item['price']/item['m2']
            price_to_m2 = (61-price_to_m2)/20
            if price_to_m2 < 0:
                price_to_m2 = 0
            #print("price: {}; m2: {}".format(item['price'], item['m2']))
        #print(price_to_m2)

        final_rating = pictures + submission_date + distance + price_to_m2
        final_rating = round(final_rating, 3)
        print("pictures: {}\nsubmission date: {}\ndistance: {}\nprice to m2: {}\nfinal rating: {}\n".format(pictures, submission_date, distance, price_to_m2, final_rating))
    
        with connection.cursor() as cursor:
            sql = "UPDATE `wroflats_submissions` SET `rating`=%s, `rating_date`=%s WHERE `id`=%s"
            f = '%Y-%m-%d %H:%M:%S'
            rating_date = datetime.datetime.now().strftime(f)
            cursor.execute(sql, (final_rating, rating_date, item['id']))
            connection.commit()
            cursor.close()
            print("Ranking updated")
