import json

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserArrivalAccessMixin
from .models import Arrival, Material
from .serializers import MaterialSerializer
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
            arrival_info['net_weight_kg'] = float(arrival_info['gross_weight_kg']) - float(arrival_info['tare_kg'])
            new_arrival = Arrival(**arrival_info)
            new_arrival.save()
            return Response({"result": "success"}, status=200)
        except Exception as e:
            print(e)
            return Response({"result": "failed"}, status=400)


class MaterialAPI(APIView):
    def get(self, request):
        if "id" in request.data:
            material = get_object_or_404(Material, id=request.data["id"])
            result = MaterialSerializer(material).data
        else:
            materials = get_list_or_404(Material)
            result = MaterialSerializer(materials, many=True).data

        return Response({"result": result})

    def post(self, request):
        try:
            material_info = request.data
            material_info['price_per_kg'] = float(material_info['price_per_kg'])
            new_material = Material(**material_info)
            new_material.save()
            return Response({"result": MaterialSerializer(new_material).data})
        except Exception as e:
            print(e)
            return Response({"result": "Failed to create new material"}, status=400)

    def put(self, request):
        try:
            material_id = request.data["id"]
            Material.objects.filter(id=material_id).update(**request.data)
            return Response({"result": "success"})
        except Exception as e:
            return Response({"result": "failed"}, status=400)

    def delete(self, request):
        material_id = request.data["id"]
        material = Material.objects.filter(id=material_id).first()
        if material:
            material.delete()
            return Response({"result": "success"})
        else:
            return Response({"result": "material no exist"}, status=400)