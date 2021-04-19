from rest_framework import serializers

from .models import Payout
from arrival.models import Arrival, ArrivalPos
from arrival.serializers import ArrivalInPayoutSerializerList, ArrivalInPayoutSerializerDetail, ArrivalPosSerializer
from office.serializers import UserSerializer, CustomerDetailSerializer


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


class ArrivalForReportSerializer(serializers.ModelSerializer):
    customer = CustomerDetailSerializer()
    arrival_pos = ArrivalPosSerializer(many=True)

    class Meta:
        model = Arrival
        fields = ['customer', 'arrival_pos']


class PayoutReportSerializer(serializers.ModelSerializer):
    arrival = ArrivalForReportSerializer()

    class Meta:
        model = Payout
        fields = ['id', 'arrival', 'vat_amount']

