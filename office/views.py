import json
from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import ScrappyUser, Customer, Rights
from .serializers import UserSerializer

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


class UserUpdateView(View):
    def post(self, request, *args, **kwargs):
        user_id = kwargs["id"]
        user = ScrappyUser.objects.filter(id=user_id)
        if user:
            request_data = json.loads(request.body)
            office_right = request_data.pop("office", False)
            payout_right = request_data.pop("payout", False)
            arrival_right = request_data.pop("arrival", False)
            Rights.objects.update_rights(user.first(),
                                         Office=office_right,
                                         Payout=payout_right,
                                         Arrival=arrival_right)
            user.update(**request_data)
            return JsonResponse({'result': 'success'})
        else:
            return JsonResponse({'result': 'User not found'}, status=404)
