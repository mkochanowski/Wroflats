import os
import pymysql.cursors
import random
import string
from os.path import join, dirname
from dotenv import load_dotenv

if os.path.isfile('.env'):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

def rand_str(length):
    return ''.join(
        random.choice(string.ascii_uppercase) for i in range(length))

def connect():
    connection = pymysql.connect(host=os.environ['DB_HOST'],
                             user=os.environ['DB_USER'],
                             password=os.environ['DB_PASS'],
                             db=os.environ['DB_NAME'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

# Connect to the database
connection = connect()