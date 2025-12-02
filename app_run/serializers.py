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

class AthleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'last_name', 'first_name']


class RunReadSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer(read_only=True)

    class Meta:
        model = Run
        fields = '__all__'

class RunWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'created_at', 'comment']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['athlete'] = self.context['request'].user
        return super().create(validated_data)
