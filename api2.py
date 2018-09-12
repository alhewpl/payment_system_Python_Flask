from flask import Flask
from flask_restful import Api, Resource, reqparse
from flaskext.mysql import MySQL
import sys

mysql = MySQL()
app = Flask(__name__)

mysql.init_app(app)
api = Api(app)

class Database():
    def __init__(self, host, user, passw, db):
        try:
            self.con = mysql.connect(host, user, passw, db)
            self.cursor = self.con.cursor()
            self.parser = reqparse.RequestParser()
            self.parser.add_argument('transaction_id', type=int)
            self.parser.add_argument('amount', type=float)
            self.parser.add_argument('timestamp', type=str)
            self.args = parser.parse_args()

            self.transactionId = self.args['transaction_id']
            self.amount = self.args['amount']
            self.timestamp = self.args['timestamp']
        except mysql.Error as e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)


#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'just_testing'
#app.config['MYSQL_DATABASE_DB'] = 'wave_payments'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config["DEBUG"] = True





#class payin(Resource):
    def payin(self):
        try:
            
            self.cursor.callproc('sp_CreateTransaction',(_transactionId,_amount,_timestamp))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return {'StatusCode':'200','Message': 'OK'}
                pass
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

#class payout(Resource):
    def payout(self):
        try:
            
            self.cursor.callproc('sp_TransactionOut',(_transactionId,_amount,_timestamp))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return {'StatusCode':'200','Message': 'OK'}
                pass
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

#class transactions(Resource):
    def get(self, transaction_id):
        conn = mysql.connect()
        cur = conn.cursor()
        
        query = '''select * from wave_payments.payins where transaction_id=%s
                union all
                select * from wave_payments.payouts where transaction_id=%s'''
        result = cur.execute(query, (transaction_id, transaction_id))
        data = cur.fetchall()
        return {"payins": {"amount" : data[0][1], "timestamp" :str(data[0][2])}, 
                "payouts": {"amount" : data[1][1], "timestamp" :str(data[1][2])}
                }        
        

    api.add_resource(payin, '/payins')
    api.add_resource(payout, '/payouts')
    api.add_resource(transactions, '/transactions/<int:transaction_id>')

if __name__ == '__main__':
    db = Database('localhost', 'root', 'just_testing', 'wave_payments')
    db.payin()
    db.payout()
    #app.run()            



