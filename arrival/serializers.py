from rest_framework import serializers
from .models import Arrival, ArrivalPos, Material


class ArrivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arrival
        fields = '__all__'


class ArrivalPosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalPos
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class ArrivalInPayoutSerializerList(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    material = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Arrival
        fields = ['id', 'customer', 'city', 'material', 'net_weight_kg', 'arrived_at', 'price']

    def get_customer(self, obj):
        return "{} {}".format(obj.customer.firstname, obj.customer.lastname)

    def get_city(self, obj):
        return obj.customer.city

    def get_material(self, obj):
        return obj.material.name

    def get_price(self, obj):
        return obj.net_weight_kg * obj.material.price_per_kg


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
