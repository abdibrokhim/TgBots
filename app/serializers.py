from rest_framework import serializers
from .models import TGClient


class TGClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = TGClient
        fields = ['tg_id', 'created_at']
