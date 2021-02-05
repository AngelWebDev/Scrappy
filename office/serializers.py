from rest_framework import serializers
from .models import ScrappyUser, Customer, Identification, Company

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappyUser
        fields = ['id', 'email', 'firstname', 'lastname', 'status']


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'firstname', 'lastname', 'street', 'city', 'title', 'vat_id', 'status']


class CustomerDetailSerializer(serializers.ModelSerializer):
    identification = IdentificationSerializer()
    company = CompanySerializer()

    class Meta:
        model = Customer
