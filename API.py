from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import datetime

app = Flask(__name__)
api = Api(app)

db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")

cursor = db.cursor()

loginTime = {}

def addLoginTime(key, value):
    loginTime[key] = value

def checkLoginTime(key):
    if(loginTime.get(key)):
        print('here')
        logoutTime = loginTime.get(key) + datetime.timedelta(minutes = 2)
        print('login:')
        print(logoutTime)
        print('current login:')
        print(datetime.datetime.now())

        if datetime.datetime.now() < logoutTime:
            addLoginTime(key, datetime.datetime.now())
        else:
            del loginTime[key]
            query = "UPDATE accounts SET login = 0 WHERE iban = %s;"
            cursor.execute(query, key)
            db.commit()



def isAccountValid(dataInput):
    query = "SELECT valid FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
    cursor.execute(query, dataInput)
    return cursor.fetchone()[0]

def isLoggedIn(dataInput):
    query = "SELECT login FROM accounts WHERE iban = %s;"
    cursor.execute(query, dataInput)
    return cursor.fetchone()[0]

class CheckIfRegistered(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)
            query = "SELECT firstName FROM customer WHERE customerID = (SELECT customerID FROM accounts WHERE iban = %s);"
            cursor.execute(query, dataInput)
            iban = cursor.fetchone()

            if(iban):
                if(isAccountValid(dataInput)):
                    return 'OK', 208
                else :
                    return 'Account blocked', 434
            else :
                return 'Account not registered', 433

        except Exception as e:
            print(e)
            return 'Json wrong', 432

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        parser.add_argument('pincode', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)

            if isAccountValid(dataInput):
                query = "SELECT pinCode FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                cursor.execute(query, dataInput)
                pinCodeData = cursor.fetchone()

                if(pinCodeData[0] == str(args.get('pincode'))):
                    query = "UPDATE accounts SET login = 1 WHERE iban = %s;"
                    cursor.execute(query, dataInput)
                    db.commit()
                    query = "UPDATE card SET noOfTries = 0 WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                    cursor.execute(query, dataInput)
                    db.commit()
                    addLoginTime(dataInput, datetime.datetime.now())
                    return 'OK', 208
                else:
                    query = "SELECT noOfTries FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                    cursor.execute(query, dataInput)
                    noOfTries = int(cursor.fetchone()[0])
                    noOfTries += 1
                    print(noOfTries)
                    dataInputTuple = (noOfTries, dataInput)
                    if noOfTries >= 3:
                        query = "UPDATE card SET noOfTries = %s, valid = 0 WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                        cursor.execute(query, dataInputTuple)
                        db.commit()
                        return 'Account blocked', 434
                    else :
                        query = "UPDATE card SET noOfTries = %s WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
                        cursor.execute(query, dataInputTuple)
                        db.commit()
                        return 'Pincode wrong', 435
            else :
                return 'Account blocked', 434
        except Exception as e:
            print(e)
            return 'Json wrong', 432

class CheckAttempts(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)
            query = "SELECT noOfTries FROM card WHERE cardID = (SELECT cardID FROM accounts WHERE iban = %s);"
            cursor.execute(query, dataInput)
            noOfTries = int(cursor.fetchone()[0])
            triesLeft = 3 - noOfTries
            return triesLeft, 208
        except Exception as e:
            print(e)
            return 'Json wrong', 432 # Bad request

class Withdraw(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('IBAN', required=True)
        parser.add_argument('amount', required = True)
        args = parser.parse_args()
        try:
            if int(args.get('amount')) <= 0:
                raise ValueError()
            
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)

            if isLoggedIn(dataInput):
                query = "SELECT balance FROM accounts WHERE iban = %s;"
                cursor.execute(query, dataInput)
                oldAmount = int(cursor.fetchone()[0])
                newAmount = oldAmount - int(args.get('amount'))

                if newAmount < 0:
                    return 'Balance too low', 437

                
                query = "UPDATE accounts SET balance = %s WHERE iban = %s;"
                dataInputTuple = (newAmount, dataInput)
                cursor.execute(query, dataInputTuple)
                db.commit()
                return {}, 208
            else:
                return 'Not logged in', 436
            
        except Exception as e:
            print(e)
            return 'Json wrong', 432 # Bad request

    
class CheckBalance(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)

            if isLoggedIn(dataInput):
                query = "SELECT balance FROM accounts WHERE iban = %s;"
                cursor.execute(query, dataInput)
                amount = float(cursor.fetchone()[0])
                return amount, 208
            else :
                return 'Not logged in', 436
        except Exception as e:
            print(e)
            return 'Json wrong', 432 # Bad request

class Logout(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('IBAN', required=True)
        args = parser.parse_args()
        try:
            dataInput = str(args.get('IBAN'))
            checkLoginTime(dataInput)
            query = "UPDATE accounts SET login = 0 WHERE iban = %s;"
            cursor.execute(query, dataInput)
            db.commit()
            return 'OK', 208
        except Exception as e:
            print(e)
            return 'Json wrong', 432 # Bad request



api.add_resource(CheckIfRegistered, '/checkIfRegistered') 
api.add_resource(Login, '/login')
api.add_resource(CheckAttempts, '/checkAttempts') 
api.add_resource(Withdraw, '/withdraw')
api.add_resource(CheckBalance, '/checkBalance')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=8050, debug=True)
