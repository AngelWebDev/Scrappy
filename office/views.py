import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import ScrappyUser, Customer


class UserView(View, LoginRequiredMixin):
    template = 'office.html'
    model = ScrappyUser

    def get(self, request):
        users = self.model.objects.exclude(status=self.model.StatusChoices.DEACTIVATED).all()
        context = {"users": users}
        return render(request, self.template, context)
