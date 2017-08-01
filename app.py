import config
import json
import datetime
from flask import Flask, request, make_response, g
from flask_restful import Resource, Api, reqparse
from json import dumps
from werkzeug.contrib.cache import SimpleCache

print("app.py initialize")
#connection = config.connection

app = Flask(__name__)
api = Api(app)
cache = SimpleCache()

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, default=datetime_handler), code)
    resp.headers.extend(headers or {})
    return resp

@app.before_request
def before_request():
    print('executed connect')
    g.db = config.connect()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        print('executed close')
        g.db.close()

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging import Formatter
    mail_handler = SMTPHandler('127.0.0.1',
                               'root@wroflats.xememah.com',
                               'askxememah@gmail.com', 'Wroflats has failed Failed')
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, datetime.date):
        return x.isoformat()
    raise TypeError("Unknown type")

class Index(Resource):
    def get(self):
        return 'wroflats made by Marek Kochanowski'

class SubmissionsIndex(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('categories', default='flats', required=False, type=str)
        parser.add_argument('page', default=1, required=False, type=int)
        args = parser.parse_args()
        
        page = args['page']-1

        if args['categories'] == 'all':
            categories = ''
        elif args['categories'] == 'flats':
            categories = "AND `category`='gumtree-flats' "
        elif args['categories'] == 'rooms':
            categories = "AND `category`='gumtree-rooms' "

        cname = "submissions-p{}-c{}".format(page, categories)
        
        pagination = ""
        if page>0:
            pagination = "{}, ".format(page*30)

        rv = cache.get(cname)
        #rv = None
        if rv is None:
            with g.db.cursor() as cursor:
                sql = "SELECT * FROM `wroflats_submissions` WHERE `deactivated`=0 AND `price` <= 2200 {}ORDER BY `rating` DESC LIMIT {}30".format(categories, pagination)
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()

                rv = result
                cache.set(cname, rv, timeout=30)
        return rv

class Submission(Resource):
    def get(self, hash):
        cname = "submission-{}".format(hash)
        
        rv = cache.get(cname)
        if rv is None:
            with g.db.cursor() as cursor:
                sql = "SELECT * FROM `wroflats_submissions` WHERE `hash`=%s LIMIT 1"
                cursor.execute(sql, hash)
                result = cursor.fetchone()
                cursor.close()
                
                rv = result
                cache.set(cname, rv, timeout=30)
        return rv  

class Token(Resource):
    def get(self, token):
        with g.db.cursor() as cursor:
            sql = "SELECT * FROM `wroflats_tokens` WHERE `token`=%s ORDER BY `created_date` DESC LIMIT 1"
            cursor.execute(sql, token)
            result = cursor.fetchone()
            if result:
                sql = "SELECT `name` FROM `wroflats_users` WHERE `id`=%s LIMIT 1"
                cursor.execute(sql, result['user_id'])
                result = cursor.fetchone()
                return {'status': 'ok', 'name': result['name']}
            else:
                return {'status': 'failed'}

class Authorize(Resource):
    def post(self):
        pin = request.json['pin']
        with g.db.cursor() as cursor:
            sql = "SELECT `id` FROM `wroflats_users` WHERE `access_code`=%s LIMIT 1"
            cursor.execute(sql, pin)
            result = cursor.fetchone()

            if result: 
                user_id = result['id']
                sql = "SELECT * FROM `wroflats_tokens` WHERE `user_id`=%s ORDER BY `created_date` DESC LIMIT 1"
                cursor.execute(sql, user_id)
                result = cursor.fetchone()

                print(result)
                if result:
                    token = result['token']
                else:
                    token = config.rand_str(20)
                    sql = "INSERT INTO `wroflats_tokens` (`user_id`, `token`) VALUES (%s, %s)"
                    cursor.execute(sql, (user_id, token))
                    g.db.commit()       
                cursor.close()

                return {'status': 'ok', 'token': token }
            else:
                return {'status': 'failed'}

api.add_resource(Submission, '/submissions/<string:hash>')
api.add_resource(SubmissionsIndex, '/submissions/')
api.add_resource(Authorize, '/auth/')
api.add_resource(Token, '/token/<string:token>')
api.add_resource(Index, '/')

if __name__ == '__main__':
    app.run(debug=True)
