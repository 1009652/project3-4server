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
            dataInput = str(args.get('IBAN'))
            query = "SELECT firstName FROM customer WHERE customerID = (SELECT customerID FROM accounts WHERE iban = %s);"
            cursor.execute(query, dataInput)
            dataRecieved = cursor.fetchone()
            if(dataRecieved):
                return {'data':dataRecieved}, 208
            else :
                return {}, 433
        except:
            return {'error': 'no data available'}, 400
    pass

class CheckAttempts(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            query = "SELECT noOfTries FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
            cursor.execute(query, dataInput)
            dataRecieved = cursor.fetchone()
            triesLeft = 3 - int(dataRecieved[0])
            return {'data': triesLeft}, 208
        except:
            return {'error': 'invalid input'}, 400 # Bad request
    pass
    
api.add_resource(CheckIfRegistered, '/checkIfRegistered') 
api.add_resource(CheckAttempts, '/checkAttempts') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050) 
