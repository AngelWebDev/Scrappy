import json

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserArrivalAccessMixin
from .models import Arrival
from office.models import Rights, ScrappyUser
from office.serializers import UserSerializer, CustomerListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class ArrivalView(LoginRequiredMixin, UserArrivalAccessMixin, View):
    template = 'arrival.html'

    def get(self, request):
        # send logged in user's data including rights info
        rights = list(Rights.objects.filter(user=request.user).values_list("right", flat=True))
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
        user = ScrappyUser.objects.filter(id=request.user.id).first()
        user_serialized = UserSerializer(user)
        user_detail.update(user_serialized.data)
        context = {
            "user": json.dumps(user_detail)
        }

        return render(request, self.template, context)


class ArrivalAPI(APIView):
    def post(self, request):
        try:
            arrival_info = request.data
            arrival_info['user_id'] = request.user.id
            arrival_info['net_weight_kg'] = arrival_info['gross_weight_kg'] - arrival_info['tare_kg']
            new_arrival = Arrival(**arrival_info)
            new_arrival.save()
            return Response({"result": "success"}, status=200)
        except Exception as e:
            return Response({"result": "failed"}, status=400)
