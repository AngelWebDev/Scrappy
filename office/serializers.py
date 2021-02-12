from rest_framework import serializers
from .models import ScrappyUser, Customer, Identification, Company, CustomInvitation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappyUser
        fields = ['id', 'email', 'firstname', 'lastname', 'status']


class IdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Identification
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CustomerListSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = Customer
        fields = ['id', 'firstname', 'lastname', 'street', 'city', 'title', 'comments', 'status', 'company']


class CustomerDetailSerializer(serializers.ModelSerializer):
    identification = IdentificationSerializer()
    company = CompanySerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomInvitation
        fields = ['id', 'email', 'firstname', 'lastname', 'office', 'arrival', 'payout']
