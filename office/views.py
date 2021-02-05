import json
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import ScrappyUser, Customer, Rights
from .serializers import UserSerializer, CustomerListSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response


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
        print(context)
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
            return Response({"result": "User not found"}, status=404)

    def delete(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data["id"]
        user = ScrappyUser.objects.filter(id=user_id)
        if user:
            user.delete()
            return Response({"result": "success"})
        else:
            return Response({"result": "User not found"}, status=404)


