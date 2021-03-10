import json
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .mixins import UserPayoutAccessMixin
from .models import Payout
from .serializers import PayoutListSerializer, PayoutDetailSerializer, PayoutReportSerializer
from arrival.models import Arrival
from arrival.serializers import ArrivalInPayoutSerializerList, ArrivalInPayoutSerializerDetail
from office.models import Rights, ScrappyUser
from office.serializers import UserSerializer


class PayoutView(LoginRequiredMixin, UserPayoutAccessMixin, DetailView):
    template_name = 'payout.html'
    context_object_name = 'user'

    def get_object(self):
        rights = list(Rights.objects.filter(user=self.request.user).values_list("right", flat=True))
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
        user = ScrappyUser.objects.filter(id=self.request.user.id).first()
        user_serialized = UserSerializer(user)
        user_detail.update(user_serialized.data)

        return json.dumps(user_detail)


class ArrivalPayoutListAPI(LoginRequiredMixin, UserPayoutAccessMixin, ListAPIView):
    serializer_class = ArrivalInPayoutSerializerList

    def get_queryset(self):
        return Arrival.objects.filter(status=Arrival.StatusChoices.OPEN).all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"result": serializer.data})


class ArrivalPayoutRetrieveUpdateAPI(LoginRequiredMixin, UserPayoutAccessMixin, RetrieveUpdateAPIView):
    lookup_field = 'id'
    serializer_class = ArrivalInPayoutSerializerDetail

    def get_queryset(self):
        return Arrival.objects.filter(status=Arrival.StatusChoices.OPEN).all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"result": serializer.data})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = Arrival.StatusChoices.PAID
        instance.save()

        new_payout = Payout()
        new_payout.arrival = instance
        new_payout.user = request.user
        new_payout.paid_amount = self.serializer_class(instance).get_price(instance)
        new_payout.save()

        return Response({"result": "success"})


class PayoutListAPI(LoginRequiredMixin, UserPayoutAccessMixin, ListAPIView):
    queryset = Payout.objects.all()
    serializer_class = PayoutListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"result": serializer.data})


class PayoutDetailAPI(LoginRequiredMixin, UserPayoutAccessMixin, RetrieveAPIView):
    queryset = Payout.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = PayoutDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({"result": serializer.data})


class PayoutReportAPI(ListAPIView):
    serializer_class = PayoutReportSerializer

    def get_queryset(self):
        if 'date' in self.request.query_params:
            start_date = datetime.datetime.strptime(self.request.query_params['date'], "%Y-%m-%d")
            end_date = start_date + datetime.timedelta(days=1)
            return Payout.objects.filter(paid_at__range=[start_date, end_date])
        else:
            return Payout.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"result": serializer.data})