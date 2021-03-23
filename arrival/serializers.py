from functools import reduce

from rest_framework import serializers
from .models import Arrival, ArrivalPos, Material


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = '__all__'


class ArrivalPosSerializer(serializers.ModelSerializer):
    material_name = serializers.SerializerMethodField()

    class Meta:
        model = ArrivalPos
        fields = ['id', 'material_name', 'gross_weight_kg', 'tare_kg', 'net_weight_kg']

    def get_material_name(self, obj):
        return obj.material.name


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ArrivalInPayoutSerializerList(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Arrival
        fields = ['id', 'customer_id',  'customer', 'city', 'arrived_at', 'price']

    def get_customer(self, obj):
        return "{} {}".format(obj.customer.firstname, obj.customer.lastname)

    def get_city(self, obj):
        return obj.customer.city

    def get_price(self, obj):
        arrival_pos = ArrivalPos.objects.filter(arrival_id=obj.id).all()
        return reduce(lambda sum, item: sum + item.net_weight_kg * item.material.price_per_kg, arrival_pos, 0.0)


class ArrivalInPayoutSerializerDetail(ArrivalInPayoutSerializerList):
    street = serializers.CharField(source='customer.street')
    company_name = serializers.SerializerMethodField()
    zip = serializers.CharField(source='customer.zip')

    class Meta(ArrivalInPayoutSerializerList.Meta):
        fields = ArrivalInPayoutSerializerList.Meta.fields + ['street', 'company_name', 'zip']

    def get_company_name(self, obj):
        if obj.customer.company:
            return obj.customer.company.name
        else:
            return None
