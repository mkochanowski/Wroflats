import config
import json
import datetime
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from json import dumps

print("app.py initialize")
connection = config.connection

app = Flask(__name__)
api = Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps(data, default=datetime_handler), code)
    resp.headers.extend(headers or {})
    return resp

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
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `wroflats_submissions` WHERE `deactivated`=0 ORDER BY `rating` DESC LIMIT 5"
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()

            return result

class Submission(Resource):
    def get(self, hash):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `wroflats_submissions` WHERE `hash`=%s LIMIT 1"
            cursor.execute(sql, hash)
            result = cursor.fetchone()
            cursor.close()

            return result

class Token(Resource):
    def get(self, token):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `wroflats_tokens` WHERE `token`=%s ORDER BY `created_date` DESC LIMIT 1"
            cursor.execute(sql, token)
            result = cursor.fetchone()
            if result:
                return {'status': 'ok'}
            else:
                return {'status': 'failed'}

class Authorize(Resource):
    def post(self):
        pin = request.form['pin']
        with connection.cursor() as cursor:
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
                    connection.commit()       
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
    connection.close()
