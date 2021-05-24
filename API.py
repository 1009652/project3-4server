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
            iban = cursor.fetchone()
            if(iban):
                query = "SELECT vallid FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                cursor.execute(query, dataInput)
                cardIsVallid = cursor.fetchone()[0]
                if(cardIsVallid):
                    return {}, 208
                else :
                    return {}, 434
            else :
                return {}, 433
        except:
            return {'error': 'json wrong'}, 432
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
            noOfTries = cursor.fetchone()
            triesLeft = 3 - int(noOfTries[0])
            return {'data': triesLeft}, 208
        except:
            return {'error': 'json wrong'}, 432 # Bad request
    pass

class Withdraw(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        parser.add_argument('amount', required = True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            query = "SELECT balance FROM accounts WHERE iban = %s;"
            cursor.execute(query, dataInput)
            oldAmount = int(cursor.fetchone()[0])
            newAmount = oldAmount - int(args.get('amount'))
            query = "UPDATE accounts SET balance = %s WHERE iban = %s;"
            dataInputTuple = (newAmount, dataInput)
            cursor.execute(query, dataInputTuple)
            db.commit()
            return {}, 208
        except:
            return {'error': 'json wrong'}, 432 # Bad request

    
class CheckBalance(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            query = "SELECT balance FROM accounts WHERE iban = %s;"
            cursor.execute(query, dataInput)
            amount = int(cursor.fetchone()[0])
            return {'data': amount}, 208
        except:
            return {'error': 'json wrong'}, 432 # Bad request



api.add_resource(CheckIfRegistered, '/checkIfRegistered') 
api.add_resource(CheckAttempts, '/checkAttempts') 
api.add_resource(Withdraw, '/withdraw')
api.add_resource(CheckBalance, '/checkBalance')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050) 
