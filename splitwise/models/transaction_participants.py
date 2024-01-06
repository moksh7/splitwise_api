from django.db import models

from splitwise.models import Transaction, SplitUser


class TransactionParticipants(models.Model):
    user = models.ForeignKey(SplitUser, on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)
    share = models.FloatField()

    class Meta:
        db_table = 'transaction_participants'