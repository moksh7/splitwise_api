# splitwise_api

APIs to keep record of User transactions and pending ledgers.


API CONTRACTS

1 CREATE USER
endpoint: /create_user
method: post
request_body: {
    'number': '123',
    'name': 'test',
    'email': 'test@test.com'
}

2 ADD TRANSACTION
According to the transaction_type relevant validations are checked and a handler is assigned to process the paylod to extract info about
the transaction.
Also after transaction has been recorded a mail to the debtor is sent asynchronously.

endpoint: /add_transaction
method: post
request_body: {  
    "payer": 3,     `# ID of user who lends`  
    "type": "3",    `# Type of transaction ('1', 'EQUAL'), ('2', 'EXACT'), ('3', 'PERCENT')`  
    "amount": 3000,  
    "share": {      `# Share of each user according to transaction_type where keys are USER IDs and values are transactional info:`  
        "1":40,         `# EQUAL: values can be 0`  
        "2": 30,        `# EXACT: exact vshare of a user in that transaction`  
        "3": 0,         `# PERCENT: percentage share of each user`  
        "4": 30
    }  
}


3 USER LEDGER
Detail about the transaction between all related users of given user_id
endpoint: /user_balance/<user_id>
method: get
params: simplify=true
response: {
    "data": [
        "a owes b : 300.0",
        "c owes b : 500.0",
        "b owes d : 1900.0"
    ]
}

{
    "data": [
        "a owes 300.0 and c owes 500.0 to b",
        "b owes 1900.0 to d"
    ]
}

4 ALL USER EXPENSES
Detail about the overall balance of all users

endpoint: /user_balances/
method: get
response: {
    "a": -1700.0,
    "b": 5300.0,
    "c": -1100.0,
    "d": -2500.0
}

CODE STRUCTURE:
project settings reside in main module.
URL for splitwise are in splitwise module.
DB schema is defined in splitwise.models module in class based format.
Serializer classes are being used to validate request data, serialize and deserialize data.
