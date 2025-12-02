from django.contrib.auth.models import User
from rest_framework import serializers

from app_run.models import Run


class UserSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'date_joined', 'username', 'last_name', 'first_name', 'type']

    def get_type(self, obj):
        if obj.is_staff:
            return 'coach'
        return 'athlete'

class RunSerializer(serializers.ModelSerializer):
    athlete_data = serializers.SerializerMethodField()

    class Meta:
        model = Run
        fields = '__all__'

    def get_athlete_data(self, obj):
        if hasattr(obj, 'athlete') and obj.athlete:
            return {
                'id': obj.athlete.id,
                'username': obj.athlete.username,
                'last_name': obj.athlete.last_name,
                'first_name': obj.athlete.first_name
            }
        return None
