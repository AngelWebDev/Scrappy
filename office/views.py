import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.core import serializers
from .models import ScrappyUser, Customer, Rights


class UserView(View, LoginRequiredMixin):
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

            user_serialized = json.loads(
                serializers.serialize("json", [user, ], fields=["email", "firstname", "lastname", "status"]))
            user_personal_info = user_serialized[0]["fields"]
            user_detail.update(user_personal_info)
            result.append(user_detail)
        print(result)
        context = {"users": json.dumps(result)}
        return render(request, self.template, context)
