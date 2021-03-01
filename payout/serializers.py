from rest_framework import serializers

from .models import Payout
from arrival.serializers import ArrivalInPayoutSerializerList, ArrivalInPayoutSerializerDetail
from office.serializers import UserSerializer


class PayoutListSerializer(serializers.ModelSerializer):
    arrival = ArrivalInPayoutSerializerList()

    class Meta:
        model = Payout
        fields = ['id', 'paid_at', 'arrival']


class PayoutDetailSerializer(serializers.ModelSerializer):
    arrival = ArrivalInPayoutSerializerDetail()
    user = UserSerializer()

    class Meta:
        model = Payout
        fields = ['id', 'paid_at', 'paid_amount', 'user', 'arrival']