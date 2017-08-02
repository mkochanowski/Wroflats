import config
import datetime

connection = config.connect()

with connection.cursor() as cursor:
    #sql = "SELECT * FROM `wroflats_submissions` WHERE `id`=2429" #debug
    sql = "SELECT * FROM `wroflats_submissions` WHERE `rating_modifier`=1 AND `full_scrap`=1 ORDER BY `rating` DESC LIMIT 1000"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    
    index = 0
    all_count = 0
    all_removed = 0
    for item in result:
        index += 1
        print("{}. id: {}, current rating: {}, rating modifier: {} ".format(index, item['id'], item['rating'], item['rating_modifier']))

        # check if was removed
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `title` FROM `wroflats_submissions` WHERE `short_desc` LIKE %s AND `rating_modifier`=0 AND `rating`=0 AND `id` <> %s"
            cursor.execute(sql, ("%"+item['short_desc']+"%", item['id']))
            removed = cursor.fetchall()
            
            if removed:
                sql = "UPDATE `wroflats_submissions` SET `rating_modifier`=0, `rating`=0 WHERE `short_desc` LIKE %s AND `rating_modifier`=1"
                cursor.execute(sql, ("%"+item['short_desc']+"%"))
                connection.commit()
                all_removed += len(removed)
                print('found removed submission!')
                print(removed)
            cursor.close()

        # check for duplicates
        with connection.cursor() as cursor:
            sql = "SELECT `id`, `title` FROM `wroflats_submissions` WHERE `short_desc` LIKE %s AND `rating_modifier`=1 AND `id` <> %s"
            cursor.execute(sql, ("%"+item['short_desc']+"%", item['id']))
            duplicates = cursor.fetchall()

            if duplicates:
                sql = "UPDATE `wroflats_submissions` SET `rating_modifier`=0.1 WHERE `short_desc` LIKE %s AND `rating_modifier`=1 AND `id` <> %s"
                cursor.execute(sql, ("%"+item['short_desc']+"%", item['id']))
                connection.commit()
                all_count += len(duplicates)
            cursor.close()
        
    print("All duplicates removed: {}, hidden: {}".format(all_count, all_removed))
    
connection.close()