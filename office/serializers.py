from rest_framework import serializers
from .models import ScrappyUser, Customer, Identification, Company, CustomInvitation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrappyUser
        fields = ['id', 'email', 'firstname', 'lastname', 'status']


class IdentificationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Identification
        exclude = ('user', )

    def get_username(self, obj):
        return "{} {}".format(obj.user.firstname, obj.user.lastname)


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
    identification = serializers.SerializerMethodField()
    company = CompanySerializer()

    class Meta:
        model = Customer
        fields = "__all__"

    def get_identification(self, obj):
        try:
            identification = Identification.objects.filter(customer=obj).latest('verified_at')
            return IdentificationSerializer(identification).data
        except Identification.DoesNotExist:
            return None



class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomInvitation
        fields = ['id', 'email', 'firstname', 'lastname', 'office', 'arrival', 'payout']
