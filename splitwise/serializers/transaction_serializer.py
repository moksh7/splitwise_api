from rest_framework import serializers

from splitwise.models import Transaction


def percent_validation(share):
    if sum(share.values()) != 100:
        raise serializers.ValidationError("percentage distribution should sum up to 100")

def exact_amount_validation(amount, share):
    if sum(share.values()) != amount:
        raise serializers.ValidationError("share distribution should sum up to total amount")


class TransactionSerializer(serializers.Serializer):
    payer = serializers.IntegerField()
    type = serializers.ChoiceField(Transaction.TRANSACTION_TYPE)
    amount = serializers.FloatField(max_value=10000000)
    share = serializers.DictField(child=serializers.FloatField())

    def validate_share(self, field):
        if len(field.keys()) > 1000:
            raise serializers.ValidationError("Only 1000 entries allowed")
        return field

    def validate(self, data):
        if data['type'] == '2':
            exact_amount_validation(data['amount'], data['share'])
        elif data['type'] == '3':
            percent_validation(data['share'])
        return data
# {i:round(j, 2) for i,j in d.items()} 