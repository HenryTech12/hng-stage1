from rest_framework.serializers import ModelSerializer
from .models import Analyzer

class AnalyzerSerializer(ModelSerializer):
    class Meta:
        model = Analyzer
        fields = '__all__'
    