from django.db import models

from splitwise.models import Transaction


class TransactionMeta(models.Model):
    note = models.CharField(max_length=500, null=True)
    amount_share = models.JSONField(null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'transaction_meta'