from rest_framework import serializers
from .models import Fingerprint

class FingerprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fingerprint
        fields = ['id', 'user_id', 'client_id', 'is_client', 'created_at', 'created_by']
