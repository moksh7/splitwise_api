from django.db import models

from splitwise.models import SplitUser


class UserBalance(models.Model):
    lender = models.ForeignKey(SplitUser, on_delete=models.DO_NOTHING, related_name='lender_set')
    debtor = models.ForeignKey(SplitUser, on_delete=models.DO_NOTHING, related_name='debtor_set')
    balance = models.FloatField(default=0)

    class Meta:
        db_table = 'user_balance'