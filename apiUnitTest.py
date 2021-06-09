import requests
import json
import unittest

import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

class testAPIChechkIfRegistered(unittest.TestCase):
    def test_normal_registered(self):
        response = requests.post('http://145.24.222.243:8050/checkIfRegistered', data={'IBAN':'NI99ABNA14789632'})
        response_data = response.status_code
        self.assertEqual(response_data, 208)
    
    def test_account_not_registered(self):
        response = requests.post('http://145.24.222.243:8050/checkIfRegistered', data={'IBAN':'NI99ABNA00000001'})
        response_data = response.status_code
        self.assertEqual(response_data, 433)

class testAPILogin(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET login = 0 WHERE customerID = 1;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET login = 0 WHERE customerID = 1;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()    

    def test_normal_login(self):
        response = requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'0bf366a6fdd643807e24b567a94e9ab1f24ef87d9353b3248e2bc42503766275'})
        response_data = response.status_code
        self.assertEqual(response_data, 208)
    
    def test_wrong_pincode_login(self):
        response = requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'1234'})
        response_data = response.status_code
        self.assertEqual(response_data, 435)
    
    def test_wrong_iban_login(self):
        response = requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA11111111', 'pincode':'1234'})
        response_data = response.status_code
        self.assertEqual(response_data, 432)
    
    def test_too_many_attempts_login(self):
        for i in range (3):
            response = requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'1234'})
        response_data = response.status_code
        self.assertEqual(response_data, 434)

class testAPICheckAttempts(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()

    def test_normal_check_attempts(self):
        response = requests.post('http://145.24.222.243:8050/checkAttempts', data={'IBAN':'NI99ABNA14789632'})
        response_data = int(response.text)
        self.assertEqual(response_data, 3)

    def test_wrong_login_attempts(self):
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'1234'})
        response = requests.post('http://145.24.222.243:8050/checkAttempts', data={'IBAN':'NI99ABNA14789632'})
        response_data = int(response.text)
        self.assertEqual(response_data, 2)
    
    def test_reset_attempts(self):
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'1234'})
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'0bf366a6fdd643807e24b567a94e9ab1f24ef87d9353b3248e2bc42503766275'})
        response = requests.post('http://145.24.222.243:8050/checkAttempts', data={'IBAN':'NI99ABNA14789632'})
        response_data = int(response.text)
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA14789632'})
        self.assertEqual(response_data, 3)

class testAPILoginBlocked(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET login = 0 WHERE customerID = 1;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 3, valid = 0 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET login = 0 WHERE customerID = 1;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 1;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()   

    def test_blocked_account_login(self):
        response = requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA14789632', 'pincode':'0bf366a6fdd643807e24b567a94e9ab1f24ef87d9353b3248e2bc42503766275'})
        response_data = response.status_code
        self.assertEqual(response_data, 434)

    def test_blocked_account_withdraw(self):
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA14789632', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 436)

class testAPICheckBalance(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 500 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA01234567', 'pincode':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'})
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 100000 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})

    def test_normal_check_balance(self):
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        response_data = float(response.text)
        self.assertEqual(response_data, 500)

    def test_not_login_check_balance(self):
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        response_data = response.status_code
        self.assertEqual(response_data, 436)

    def test_after_withdraw_check_balance(self):
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'199.5'})
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        response_data = float(response.text)
        self.assertEqual(response_data, 300.5)

class testAPIWithdraw(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 500 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA01234567', 'pincode':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'})
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 100000 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})

    def test_not_login_withdraw(self):
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 436)

    def test_balance_low_withdraw(self):
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'2000'})
        response_data = response.status_code
        self.assertEqual(response_data, 437)
    
    def test_normal_withdraw(self):
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 208)
    
    def test_negative_withdraw(self):
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'-200'})
        response_data = response.status_code
        self.assertEqual(response_data, 432)
    
    def test_amount_is_withdraw(self):
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        oldBalance = float(response.text)
        requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'200'})
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        newBalance = float(response.text)
        self.assertEqual(newBalance, (oldBalance - 200))
    
class testAPILogout(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 500 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA01234567', 'pincode':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'})
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 100000 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})

    def test_normal_logout(self):
        response = requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        response_data = response.status_code
        self.assertEqual(response_data, 208)
    
    def test_worked_logout(self):
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        response = requests.post('http://145.24.222.243:8050/withdraw', data={'IBAN':'NI99ABNA01234567', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 436)

class testAPITransfer(unittest.TestCase):
    def setUp(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 500 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA01234567', 'pincode':'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'})
        requests.post('http://145.24.222.243:8050/login', data={'IBAN':'NI99ABNA20011306', 'pincode':'f89328f7804b950087f0fabde05183a45be91aaca59f8d029bb1932bfbc87bc7'})
    
    def tearDown(self):
        db = MySQLdb.connect(host='145.24.222.243', port=8051, user="primary", passwd="Timmerman123!", db="ABNMANBRO")
        cursor = db.cursor()
        query = "UPDATE accounts SET balance = 100000 WHERE customerID = 2;"
        cursor.execute(query)
        db.commit()
        query = "UPDATE card SET noOfTries = 0, valid = 1 WHERE cardID = 0;"
        cursor.execute(query)
        db.commit()
        cursor.close()
        db.close()
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA20011306'})

    def test_not_login_transfer(self):
        requests.post('http://145.24.222.243:8050/logout', data={'IBAN':'NI99ABNA01234567'})
        response = requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 436)

    def test_balance_low_transfer(self):
        response = requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'2000'})
        response_data = response.status_code
        self.assertEqual(response_data, 437)
    
    def test_normal_transfer(self):
        response = requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'200'})
        response_data = response.status_code
        self.assertEqual(response_data, 208)
    
    def test_negative_transfer(self):
        response = requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'-200'})
        response_data = response.status_code
        self.assertEqual(response_data, 432)

    def test_amount_is_taken_transfer(self):
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        oldBalance = float(response.text)
        requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'200'})
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA01234567'})
        newBalance = float(response.text)
        self.assertEqual(newBalance, (oldBalance - 200))
    
    def test_amount_is_transfer(self):
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA20011306'})
        oldBalance = float(response.text)
        requests.post('http://145.24.222.243:8050/transfer', data={'IBAN':'NI99ABNA01234567', 'targetIBAN':'NI99ABNA20011306', 'amount':'200'})
        response = requests.post('http://145.24.222.243:8050/checkBalance', data={'IBAN':'NI99ABNA20011306'})
        newBalance = float(response.text)
        self.assertEqual(newBalance, (oldBalance + 200))
    

if __name__=='__main__':
    unittest.main()