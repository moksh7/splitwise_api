from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import connection


def get_balance_data(params):
    with connection.cursor() as cursor:
        q = '''
            SELECT lb.debtor_id, lb.balance, u.name, lu.name debtor
            FROM split_user u
            JOIN user_balance lb
            ON lb.lender_id = u.id
            JOIN split_user lu
            ON lu.id = lb.debtor_id
            where u.id=%s
            '''
        cursor.execute(q,params)
        lent_list = cursor.fetchall()
        q = '''
            SELECT db.lender_id, db.balance, u.name, lu.name lender
            FROM split_user u
            JOIN user_balance db
            ON db.debtor_id = u.id
            JOIN split_user lu
            ON lu.id = db.lender_id
            where u.id=%s
            '''
        cursor.execute(q,params)
        debt_list = cursor.fetchall()
    return lent_list, debt_list

def compile_balance_data(lent_list, debt_list):
    balance_map = {row[0]:list(row[1:]) for row in lent_list} 
    for row in debt_list:
        user_id, balance, user_name, participant_name = row
        if user_id not in balance_map:
            balance_map[user_id] = [-abs(balance), user_name, participant_name]
            continue
        balance_map[user_id][0] -= balance
    return balance_map

def segregate_expense(balance_ls):
    lent_ls, debt_ls = [], []
    for data in balance_ls:
        if data[0] > 0:
            lent_ls.append(data)
        elif data[0] < 0:
            debt_ls.append(data)
    return lent_ls, debt_ls


def get_redable_response(lent_ls, debt_ls, simplify=False):
    resp = {'data': []}
    if simplify:
        if lent_ls:
            lent_resp = ' and '.join([f'{data[2]} owes {data[0]}' for data in lent_ls])
            lent_resp = f'{lent_resp} to {lent_ls[0][1]}'
            resp['data'].append(lent_resp)
        if debt_ls:
            debt_resp = ' and '.join([f'{abs(data[0])} to {data[2]}' for data in debt_ls])
            lent_resp = f'{lent_ls[0][1]} owes {debt_resp}'
            resp['data'].append(lent_resp)
        return resp

    for data in lent_ls:
        resp['data'].append(f'{data[2]} owes {data[1]} : {data[0]}')
    for data in debt_ls:
        resp['data'].append(f'{data[1]} owes {data[2]} : {abs(data[0])}')
    return resp
    



class UserExpenseView(APIView):
    
    def get(self, request, user_id):   
        balance_map = compile_balance_data(*get_balance_data([user_id]))
        simplify =True if request.query_params.get('simplify') == 'true' else False
        resp = get_redable_response(*segregate_expense(balance_map.values()), simplify=simplify)
        return Response(resp)