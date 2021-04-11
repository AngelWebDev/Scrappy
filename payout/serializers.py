from rest_framework import serializers

from .models import Payout
from arrival.models import Material
from arrival.serializers import ArrivalInPayoutSerializerList, ArrivalInPayoutSerializerDetail, MaterialSerializer
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


class PayoutReportSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()
    price_per_kg = serializers.SerializerMethodField()
    net_weight = serializers.SerializerMethodField()

    class Meta:
        model = Payout
        fields = ['id', 'customer', 'material', 'price_per_kg', 'net_weight', 'vat_amount']

    def get_price_per_kg(self, obj):
        return obj.arrival.arrival_pos.price_per_kg

    def get_net_weight(self, obj):
        return obj.arrival.net_weight_kg

    def get_customer(self, obj):
        return CustomerDetailSerializer(obj.arrival.customer).data

