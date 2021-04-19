from functools import reduce

from rest_framework import serializers
from .models import Arrival, ArrivalPos, Material


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = '__all__'


class ArrivalPosSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = ArrivalPos
        fields = ['id', 'material', 'gross_weight_kg', 'tare_kg', 'net_weight_kg']


class ArrivalInPayoutSerializerList(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    city = serializers.CharField(source='customer.city')
    price = serializers.SerializerMethodField()

    class Meta:
        model = Arrival
        fields = ['id', 'customer_id',  'customer', 'city', 'arrived_at', 'price']

    def get_customer(self, obj):
        return "{} {}".format(obj.customer.firstname, obj.customer.lastname)

    def get_price(self, obj):
        arrival_pos = ArrivalPos.objects.filter(arrival_id=obj.id).all()
        return reduce(lambda sum, item: sum + item.net_weight_kg * item.material.price_per_kg, arrival_pos, 0.0)


class ArrivalInPayoutSerializerDetail(ArrivalInPayoutSerializerList):
    street = serializers.CharField(source='customer.street')
    identification = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    zip = serializers.CharField(source='customer.zip')
    arrival_pos = ArrivalPosSerializer(many=True)

    class Meta(ArrivalInPayoutSerializerList.Meta):
        fields = ArrivalInPayoutSerializerList.Meta.fields + ['street', 'company_name', 'zip', 'identification', 'arrival_pos']

    def get_company_name(self, obj):
        if obj.customer.company:
            return obj.customer.company.name
        else:
            return None

    def get_identification(self, obj):
        return obj.customer.identifications.exists()
