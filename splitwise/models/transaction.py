from django.db import models

from splitwise.models import SplitUser


class Transaction(models.Model):
    TRANSACTION_TYPE = (('1', 'EQUAL'), ('2', 'EXACT'), ('3', 'PERCENT'))
    transaction_type = models.CharField(choices=TRANSACTION_TYPE)
    amount = models.FloatField()
    payer = models.ForeignKey(SplitUser, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'transaction'
