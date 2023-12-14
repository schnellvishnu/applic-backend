from reportapp.models import ProductionReport
from rest_framework import serializers

class ProductionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionReport
        fields = "__all__"