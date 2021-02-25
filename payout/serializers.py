from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payout
from arrival.models import Material, Arrival
from office.models import Customer


