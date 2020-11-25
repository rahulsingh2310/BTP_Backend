from . models import *
from rest_framework import serializers


class GasSerializer(serializers.ModelSerializer):
    class meta:
        model = GasDetails
        fields = "__all__"
