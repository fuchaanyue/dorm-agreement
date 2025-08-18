from rest_framework import serializers
from .models import AgreementRecord, AgreementSupplement

class AgreementRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgreementRecord
        fields = '__all__'

class AgreementSupplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgreementSupplement
        fields = '__all__'
