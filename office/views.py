import json
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.views.generic import View
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ScrappyUser, Customer, Rights, Company
from .serializers import UserSerializer, CustomerListSerializer, CustomerDetailSerializer
from .forms import UserSignUpForm


def signup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = ScrappyUser.objects.create_user(**form.cleaned_data)
            login(request, user)
            return redirect('office_view')
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class OfficeView(View, LoginRequiredMixin):
    template = 'office.html'

    def get(self, request):
        users = []
        users_obj = ScrappyUser.objects.exclude(status=ScrappyUser.StatusChoices.DEACTIVATED).all()

        for user in users_obj:
            rights = list(Rights.objects.filter(user=user).values_list("right", flat=True))
            user_detail = {
                "office": False,
                "payout": False,
                "arrival": False
            }

            if 'Office' in rights:
                user_detail['office'] = True
            if 'Payout' in rights:
                user_detail['payout'] = True
            if 'Arrival' in rights:
                user_detail['arrival'] = True

            user_serialized = UserSerializer(user)
            user_detail.update(user_serialized.data)
            users.append(user_detail)

        context = {"users": json.dumps(users)}

        customer_search_term = request.GET.get('customer', None)

        customers_obj = Customer.objects
        if customer_search_term:
            customers_obj = Customer.objects.filter(
                Q(firstname__contains=customer_search_term) | Q(lastname__contains=customer_search_term))

        customers_serialized = CustomerListSerializer(customers_obj.all(), many=True)
        context["customers"] = json.dumps(customers_serialized.data)

        return render(request, self.template, context)


class UserUpdateDeleteAPI(RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data["id"]
        user = ScrappyUser.objects.filter(id=user_id)

        if user:
            office_right = request_data.pop("office", False)
            payout_right = request_data.pop("payout", False)
            arrival_right = request_data.pop("arrival", False)
            Rights.objects.update_rights(user.first(),
                                         Office=office_right,
                                         Payout=payout_right,
                                         Arrival=arrival_right)
            user.update(**request_data)
            return Response({"result": "success"})
        else:
            return Response({"result": "User not found"}, status=400)

    def delete(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data["id"]
        user = ScrappyUser.objects.filter(id=user_id)
        if user:
            user.delete()
            return Response({"result": "success"})
        else:
            return Response({"result": "User not found"}, status=400)


class CustomerAPIView(APIView):
    model = Customer
    list_serializer = CustomerListSerializer
    detail_serializer = CustomerDetailSerializer
    
    def get(self, request):
        customer_id = request.query_params["id"]
        try:
            customer = self.model.objects.get(id=customer_id)
            return Response({"result": self.detail_serializer(customer).data})
        except self.model.DoesNotExist:
            return Response({"result": "Customer not found"}, status=400)

    def post(self, request):
        request_data = request.data
        print(request_data)
        try:
            company_info = request_data.pop("company")
            if company_info:
                new_company = Company(**company_info)
                new_company.save()
                request_data["company_id"] = new_company.id
            new_customer = self.model(**request_data)
            new_customer.save()
            return Response({"result": json.dumps(self.list_serializer(new_customer).data)})
        except Exception as e:
            print(e)
            return Response({"result": "Failed to create new customer"}, status=400)
    
    def put(self, request):
        request_data = request.data
        try:
            company_info = request_data.pop("company")
            self.model.objects.filter(id=request_data["id"]).update(**request_data)
            if company_info:
                Company.objects.filter(id=company_info["id"]).update(**company_info)
            return Response({"result": "success"})
        except Exception as e:
            return Response({"result": "Failed customer update"}, status=400)

    def delete(self, request):
        request_data = request.data
        try:
            self.model.objects.filter(id=request_data["id"]).delete()
            return Response({"result": "success"})
        except Exception as e:
            return Response({"result": "Failed customer delete"}, status=400)
