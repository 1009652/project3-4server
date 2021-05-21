from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
api = Api(app)

db = MySQLdb.connect(host="remotemysql.com", user="5J9rC1RF8E", passwd="U8IIWXIJZT", db="5J9rC1RF8E")

cursor = db.cursor()

class CheckIfRegistered(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            data = str(args.get('IBAN'))
            query = "SELECT iban FROM accounts WHERE iban = %s;"
            cursor.execute(query, data)
            if(data):
                return {}, 208
            else :
                return {}, 433
        except:
            return {'error': 'no data available'}, 400
    pass

class Withdraw2(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('name', required=True)
        args = parser.parse_args()
        try:
            # do stuff here
            name = "Hello " + str(args.get('name'))
            return {'data' : name}, 200 # OK
        except:
            return {'error': 'invalid input'}, 400 # Bad request
    pass
    
api.add_resource(CheckIfRegistered, '/checkIfRegistered') 
api.add_resource(Withdraw2, '/withdrawPost') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050) 
