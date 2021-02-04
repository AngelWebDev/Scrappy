import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import ScrappyUser, Customer, Rights
from .serializers import UserSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response


class UserListCreateView(View, LoginRequiredMixin):
    template = 'office.html'
    model = ScrappyUser

    def get(self, request):
        result = []
        users = self.model.objects.exclude(status=self.model.StatusChoices.DEACTIVATED).all()

        for user in users:
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
            result.append(user_detail)

        context = {"users": json.dumps(result)}
        return render(request, self.template, context)


class UserUpdateAPI(UpdateAPIView):
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
