from flask import Flask
from flask_restful import Api, Resource, reqparse
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'hidden*'
app.config['MYSQL_DATABASE_DB'] = 'wave_payments'
app.config['MYSQL_DATABASE_HOST'] = 'myhost'
app.config["DEBUG"] = True


mysql.init_app(app)
api = Api(app)


class payin(Resource):
    def post(self):
        try:
            # Parsing arguments
            parser = reqparse.RequestParser()
            parser.add_argument('transaction_id', type=int)
            parser.add_argument('amount', type=float)
            parser.add_argument('timestamp', type=str)
            args = parser.parse_args()

            _transactionId = args['transaction_id']
            _amount = args['amount']
            _timestamp = args['timestamp']
            
            conn = mysql.connect()
            cursor = conn.cursor() 
            cursor.callproc('sp_CreateTransaction',(_transactionId,_amount,_timestamp))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return {'StatusCode':'200','Message': 'OK'}
                pass
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

class payout(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('transaction_id', type=int)
            parser.add_argument('amount', type=float)
            parser.add_argument('timestamp', type=str)
            args = parser.parse_args()

            _transactionId = args['transaction_id']
            _amount = args['amount']
            _timestamp = args['timestamp']

            conn = mysql.connect()
            cursor = conn.cursor()  
            cursor.callproc('sp_TransactionOut',(_transactionId,_amount,_timestamp))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                #return {'StatusCode':'200','Message': 'OK'}
                pass
            else:
                return {'StatusCode':'1000','Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

class transactions(Resource):
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
    app.run()            



