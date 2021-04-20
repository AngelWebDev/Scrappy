import json
import datetime

from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from .mixins import UserPayoutAccessMixin
from .models import Payout
from scrappy import settings as project_setting
from .serializers import PayoutListSerializer, PayoutDetailSerializer, PayoutReportSerializer
from arrival.models import Arrival, Material, ArrivalPos
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


class ArrivalChangeCustomerAPI(LoginRequiredMixin, UserPayoutAccessMixin, RetrieveUpdateAPIView):
    serializer_class = ArrivalInPayoutSerializerDetail
    lookup_field = 'id'

    def get_queryset(self):
        return Arrival.objects.filter(status=Arrival.StatusChoices.OPEN).all()

    def update(self, request, id, customer_id):
        obj = self.get_object()
        if obj:
            obj.customer_id = customer_id
            obj.save()
            return Response({"result": self.get_serializer(obj).data})
        else:
            return Response({"result": "There is no matching arrival data"}, 404)


class PayoutListAPI(LoginRequiredMixin, UserPayoutAccessMixin, ListAPIView):
    serializer_class = PayoutListSerializer
    queryset = Payout.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"result": serializer.data})


class PayoutDetailAPI(LoginRequiredMixin, UserPayoutAccessMixin, RetrieveAPIView):
    queryset = Payout.objects.all()
    lookup_field = 'id'
    serializer_class = PayoutDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance)
        return Response({"result": serializer.data})


class PayoutReportAPI(LoginRequiredMixin, UserPayoutAccessMixin, ListAPIView):
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


class PayoutReversalAPI(LoginRequiredMixin, UserPayoutAccessMixin, APIView):
    def post(self, request, id):
        try:
            payout = Payout.objects.get(id=id)
            arrival = Arrival.objects.get(id=payout.arrival_id)
            arrival.status = Arrival.StatusChoices.OPEN
            arrival.save()
            payout.delete()
            return Response({"result": "success"}, 200)
        except Exception as e:
            print(e)
            return Response({"result": "failed"}, 400)


class PayoutReportEmailAPI(LoginRequiredMixin, UserPayoutAccessMixin, APIView):
    def post(self, request):
        id = request.data["payout_id"]
        arrival_pos_id = request.data["arrival_pos_id"]
        email = request.data["email"]
        payout = Payout.objects.get(id=id)

        if payout:
            try:
                customer = payout.arrival.customer
                arrival_pos = ArrivalPos.objects.get(id=arrival_pos_id)
                material = Material.objects.get(id=arrival_pos.material_id)
                context = {
                    "material_name": material.name,
                    "arrived_at": payout.arrival.arrived_at,
                    "net_weight": arrival_pos.net_weight_kg,
                    "total_price": arrival_pos.net_weight_kg * material.price_per_kg,
                    "customer_name": customer,
                    "company_name": customer.company.name,
                    "address": customer.street,
                    "zip": customer.zip,
                    "city": customer.city
                }

                message = get_template("payout_report.html").render(context)
                mail = EmailMessage(
                    subject="Payout Report",
                    body=message,
                    from_email=project_setting.EMAIL_HOST_USER,
                    to=[email],
                )
                mail.content_subtype = "html"
                mail.send()
                return Response({"result": "success"})
            except:
                return Response({"result": "failed"}, 400)
        else:
            return Response({"result": "failed"}, 404)