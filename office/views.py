import json

from django.urls import reverse
from django.db.models import Q
from django.db.utils import IntegrityError
from django.contrib import messages
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from invitations.app_settings import app_settings
from invitations.adapters import get_invitations_adapter
from invitations.views import AcceptInvite, accept_invitation

from .mixins import UserOfficeAccessMixin
from .models import ScrappyUser, Customer, Rights, Company, CustomInvitation, Identification
from .serializers import UserSerializer, CustomerListSerializer, CustomerDetailSerializer, InvitationSerializer
from .forms import UserSignUpForm


def scrappy_login(request):
    if request.user.is_authenticated:
        return redirect(reverse('office_view'))

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user:
            if user.status == 'Active':
                login(request, user)
                return redirect(reverse('office_view'))
            elif user.status == 'Deactivated':
                messages.error(request, 'Your account was deactivated!')
        else:
            messages.error(request, 'Email or Password not correct!')
            return redirect(reverse('login'))
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def signup(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = ScrappyUser.objects.create_user(**form.cleaned_data)
            login(request, user)

            user_rights = CustomInvitation.objects.filter(email=user.email).first()
            if user_rights.arrival:
                Rights.objects.create(user=user, right=Rights.RightChoices.ARRIVAL)
            if user_rights.office:
                Rights.objects.create(user=user, right=Rights.RightChoices.OFFICE)
            if user_rights.payout:
                Rights.objects.create(user=user, right=Rights.RightChoices.PAYOUT)

            return redirect('office_view')
    else:
        invited_user = CustomInvitation.objects.filter(key=kwargs["key"]).first()
        form = UserSignUpForm(instance=invited_user)
    return render(request, 'registration/signup.html', {'form': form})


class InviteAcceptView(LoginRequiredMixin, AcceptInvite):
    def post(self, request, *args, **kwargs):
        self.object = invitation = self.get_object()

        # No invitation was found.
        if not invitation:
            # Newer behavior: show an error message and redirect to signup.
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_invalid.txt')
            return redirect(app_settings.LOGIN_REDIRECT)

        # The invitation was previously accepted, redirect to the login
        if invitation.accepted:
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_accepted.txt',
                {'email': invitation.email})
            # Redirect to login since there's hopefully an account already.
            return render(request, 'invitations/accepted.html')

        # The key was expired.
        if invitation.key_expired():
            get_invitations_adapter().add_message(
                self.request,
                messages.ERROR,
                'invitations/messages/invite_expired.txt',
                {'email': invitation.email})
            # Redirect to sign-up since they might be able to register anyway.
            return redirect(app_settings.LOGIN_REDIRECT)

        # The invitation is valid.
        # Mark it as accepted now if ACCEPT_INVITE_AFTER_SIGNUP is False.
        if not app_settings.ACCEPT_INVITE_AFTER_SIGNUP:
            accept_invitation(invitation=invitation,
                              request=self.request,
                              signal_sender=self.__class__)

        get_invitations_adapter().stash_verified_email(
            self.request, invitation.email)

        return redirect('signup', key=kwargs["key"])


class UserInviteAPI(LoginRequiredMixin, APIView):
    model = CustomInvitation
    
    def post(self, request):
        try:
            invite = self.model.create(**request.data, inviter=request.user)
            invite.send_invitation(request)
        except IntegrityError:
            return Response({"result": "Invitation already sent"}, status=400)
        return Response({"result": "success"})

    def delete(self, request):
        email = request.data["email"]
        try:
            invitation = self.model.objects.get(email=email)
            invitation.delete()
            return Response({"result": "success"})
        except self.model.DoesNotExist:
            return Response({"result": "No invitation exists"}, status=400)


class OfficeView(LoginRequiredMixin, UserOfficeAccessMixin, View):
    template = 'office.html'

    def get(self, request):
        print(Rights.RightChoices)
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


class UserAPI(LoginRequiredMixin, RetrieveUpdateDestroyAPIView):
    def retrieve(self, request, *args, **kwargs):
        users = []
        try:
            users_obj = ScrappyUser.objects.filter(status=ScrappyUser.StatusChoices.ACTIVE).all()
            if users_obj:
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

                invited_users = CustomInvitation.objects.filter(accepted=0).all()
                pending_users = []
                for iuser in invited_users:
                    if not iuser.key_expired():
                        invited_user_serialize = InvitationSerializer(iuser).data
                        invited_user_serialize['status'] = 'Pending'
                        pending_users.append(invited_user_serialize)

                users.extend(pending_users)
                return Response({"result": users})
            else:
                return Response({"result": "No User"}, status=204)
        except:
            return Response({"result": ""}, status=400)

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
            return Response({"result": "User not found"}, status=400)

    def delete(self, request, *args, **kwargs):
        request_data = request.data
        user_id = request_data["id"]
        user = ScrappyUser.objects.filter(id=user_id)
        if user:
            user.delete()
            return Response({"result": "success"})
        else:
            return Response({"result": "User not found"}, status=400)


class CustomerAPIView(LoginRequiredMixin, APIView):
    model = Customer
    list_serializer = CustomerListSerializer
    detail_serializer = CustomerDetailSerializer

    def get(self, request):
        customer_id = request.query_params.get("id", None)
        customer_search_term = request.query_params.get('customer', None)

        if customer_id:
            try:
                customer = self.model.objects.get(id=customer_id)
                return Response({"result": self.detail_serializer(customer).data})
            except self.model.DoesNotExist:
                return Response({"result": "Customer not found"}, status=400)

        customers_obj = Customer.objects
        if customer_search_term:
            customers_obj = customers_obj.filter(
                Q(firstname__contains=customer_search_term) | Q(lastname__contains=customer_search_term))

        customers_serialized = CustomerListSerializer(customers_obj.all(), many=True)
        return Response({"result": customers_serialized.data})

    def post(self, request):
        request_data = request.data
        try:
            company_info = request_data.pop("company")
            if company_info:
                new_company = Company(**company_info)
                new_company.save()
                request_data["company_id"] = new_company.id

            identification_info = request_data.pop("identification")
            if identification_info:
                new_identification = Identification(**identification_info)
                new_identification.user = request.user
                new_identification.save()
                request_data["identification_id"] = new_identification.id

            new_customer = self.model(**request_data)
            new_customer.save()
            return Response({"result": self.list_serializer(new_customer).data})
        except Exception as e:
            print(e)
            return Response({"result": "Failed to create new customer"}, status=400)

    def put(self, request):
        request_data = request.data
        try:
            company_info = request_data.pop("company")
            identification_info = request_data.pop("identification")
            self.model.objects.filter(id=request_data["id"]).update(**request_data)
            if company_info:
                Company.objects.filter(id=company_info["id"]).update(**company_info)
            if identification_info:
                Identification.objects.filter(user=request.user).update(**identification_info)
            return Response({"result": "success"})
        except Exception as e:
            return Response({"result": "Failed customer update"}, status=400)

    def delete(self, request):
        request_data = request.data
        try:
            self.model.objects.filter(id=request_data["id"]).delete()
            return Response({"result": "success"})
        except Exception as e:
            return Response({"result": "Failed customer delete"}, status=400)
