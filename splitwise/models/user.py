from django.db import models


class SplitUser(models.Model):
    name = models.CharField(max_length=100) 
    email = models.EmailField()
    number = models.CharField(max_length=15, unique=True)
    amount_lent = models.FloatField(default=0)
    amount_owed = models.FloatField(default=0)

    class Meta:
        db_table = 'split_user'