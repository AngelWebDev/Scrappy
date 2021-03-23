import json
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .mixins import UserArrivalAccessMixin
from .models import Arrival, ArrivalPos, Material
from .serializers import MaterialSerializer, ArrivalPosSerializer
from office.models import Rights, ScrappyUser
from office.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
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


class ArrivalListCreateAPI(LoginRequiredMixin, UserArrivalAccessMixin, ListCreateAPIView):
    serializer_class = ArrivalPosSerializer

    def list(self, request, *args, **kwargs):
        try:
            arrival_pos = ArrivalPos.objects.filter(
                arrival__customer_id=request.query_params['customer_id'],
                arrival__status=Arrival.StatusChoices.OPEN
            ).order_by('-arrival__arrived_at').all()
            if arrival_pos:
                context = {"result": ArrivalPosSerializer(arrival_pos, many=True).data}
                return Response(context, status=200)
            else:
                return Response({"result": "No Content"}, status=204)
        except:
            return Response({"result": "failed"}, status=400)

    def create(self, request, *args, **kwargs):
        try:
            arrival_pos = request.data
            customer_id = arrival_pos.pop('customer_id')
            shipment_time = arrival_pos.pop('arrived_at')
            arrival, is_created = Arrival.objects.get_or_create(
                customer_id=customer_id, user=request.user, arrived_at=shipment_time)
            arrival_pos['net_weight_kg'] = Decimal(arrival_pos['gross_weight_kg']) - Decimal(arrival_pos['tare_kg'])
            arrival_pos['arrival_id'] = arrival.id
            new_arrival_pos = ArrivalPos(**arrival_pos)
            new_arrival_pos.save()
            return Response({"result": self.serializer_class(new_arrival_pos).data}, status=200)
        except Exception as e:
            print(e)
            return Response({"result": "failed"}, status=400)


class ArrivalPosDestroyAPI(LoginRequiredMixin, UserArrivalAccessMixin, DestroyAPIView):
    queryset = ArrivalPos.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            remove_obj = self.get_object()
            remove_obj.delete()

            # Remove Arrival data if belonged ArrivalPos data is empty
            arrival_pos = ArrivalPos.objects.filter(arrival_id=remove_obj.arrival_id).all()
            if not arrival_pos:
                Arrival.objects.filter(id=remove_obj.arrival_id).delete()

            return Response({"result": "success"}, status=200)
        except:
            return Response({"result": "failed"}, status=400)


class MaterialAPI(LoginRequiredMixin, UserArrivalAccessMixin, APIView):
    def get(self, request):
        if "id" in request.query_params:
            material = get_object_or_404(Material, id=request.query_params.get("id"))
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