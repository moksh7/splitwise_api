from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView

from splitwise.views.user_expense_view import compile_balance_data

def get_balance_data():
    with connection.cursor() as cursor:
        q = '''
            SELECT u.id, u.name, SUM(lb.balance)
            FROM split_user u
            JOIN user_balance lb
            ON lb.lender_id = u.id
            GROUP BY u.id
            '''
        cursor.execute(q)
        lent_list = cursor.fetchall()

        q = '''
            SELECT u.id, u.name, SUM(db.balance)
            FROM split_user u
            JOIN user_balance db
            ON db.debtor_id = u.id
            GROUP BY u.id
            '''
        cursor.execute(q)
        debt_list = cursor.fetchall()
        print(lent_list, debt_list)
    return lent_list, debt_list

def compile_balance_data(lent_list, debt_list):
    balance_map = {row[0]:list(row[1:]) for row in lent_list} 
    for row in debt_list:
        user_id, user_name, balance = row
        if user_id not in balance_map:
            balance_map[user_id] = [user_name, -abs(balance)]
            continue
        balance_map[user_id][1] -= balance
    return balance_map

def get_resp(balance):
    resp = {}
    for id in balance:
        if balance[id][1] != 0:
            resp[balance[id][0]] = balance[id][1]
    return resp

class UserBalances(APIView):
    
    def get(self, request):   
        balance = compile_balance_data(*get_balance_data())
        print(balance)
        return Response(get_resp(balance))