from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Withdraw(Resource): # GET
    def get(self):
        try:
            #do stuff here
            newBalance = 300 - 70
            return {'data': newBalance}, 200
        except:
            return {'error': 'no data available'}, 400
    pass

class Withdraw2(Resource): # POST
    def post(self):
        parser = reqparse.RequestParser() 
        parser.add_argument('money', required=True)
        args = parser.parse_args()
        try:
            # do stuff here
            money = int(args.get('money'))
            newBalance = 300 - money
            return {'data' : newBalance}, 200 # OK
        except:
            return {'error': 'invalid input'}, 400 # Bad request
    pass
    
api.add_resource(Withdraw, '/withdrawGet') 
api.add_resource(Withdraw2, '/withdrawPost') 

if __name__ == '__main__':
    app.run() 