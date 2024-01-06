from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from splitwise.models import Transaction, UserBalance
from splitwise.serializers import TransactionSerializer
from splitwise.utils import send_html_mail


class AddTransactionView(GenericAPIView):
    serializer_class = TransactionSerializer
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        handlers = TranasctionHandler.get_transaction_handlers()
        transaction_handler = handlers.get(serializer.validated_data.get('type'))
        with transaction.atomic():
            transaction_handler(serializer.validated_data)
        return Response({'data': 'Successsss'})


class TranasctionHandler:

    @classmethod
    def get_transaction_handlers(cls):
        return {
            "1" : cls.equal_share_transaction,
            "2" : cls.exact_share_transaction,
            "3" : cls.percent_share_transaction,
        }

    @classmethod
    def add_user_balance(cls, lender_id, transaction_data):
        for user_id in transaction_data:
            user_balance = UserBalance.objects.filter(lender_id=lender_id, debtor_id=user_id).first()
            if not user_balance:
                UserBalance.objects.create(lender_id=lender_id, debtor_id=user_id, balance=transaction_data.get(user_id))
                continue
            user_balance.balance += transaction_data.get(user_id)
            user_balance.save()
            mail_body = 'Transaction of %s added to your balance by %s' % (transaction_data.get(user_id), '%s')
            send_html_mail('Splitwise Transaction', mail_body, user_id, lender_id)


    @classmethod
    def equal_share_transaction(cls, data):
        amount = data.get('amount')
        transaction_data = data.get('share')
        Transaction.objects.create(payer_id=data.get('payer'), amount=amount, transaction_type=data.get('type'))
        amount_share = round(amount / len(transaction_data), 2)

        transaction_data.pop(str(data.get('payer')))
        for user_id in transaction_data:
            transaction_data[user_id] = amount_share
        cls.add_user_balance(data.get('payer'), transaction_data)

    @classmethod
    def exact_share_transaction(cls, data):
        amount = data.get('amount')
        transaction_data = data.get('share')
        payer_id = str(data.get('payer'))
        Transaction.objects.create(payer_id=payer_id, amount=amount, transaction_type=data.get('type'))

        transaction_data.pop(payer_id)
        cls.add_user_balance(payer_id, transaction_data)

    @classmethod
    def percent_share_transaction(cls, data):
        amount = data.get('amount')
        transaction_data = data.get('share')
        payer_id = str(data.get('payer'))
        Transaction.objects.create(payer_id=payer_id, amount=amount, transaction_type=data.get('type'))

        transaction_data.pop(payer_id)
        for user_id in transaction_data:
            user_share = (amount * transaction_data.get(user_id)) / 100
            transaction_data[user_id] = user_share
        cls.add_user_balance(payer_id, transaction_data)
