from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import render

from app_run.models import Run
from app_run.serializers import UserSerializer, RunReadSerializer, RunWriteSerializer


# Create your views here.
@api_view(['GET'])
def company_details(request):
    details = {
        'company_name': settings.COMPANY_NAME,
        'slogan': settings.SLOGAN,
        'contacts': settings.CONTACTS
    }
    return Response(details)

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.select_related('athlete').all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RunReadSerializer
        return RunWriteSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        user_type = self.request.query_params.get('type')
        if user_type == 'coach':
            qs = qs.filter(is_staff=True)
        elif user_type == 'athlete':
            qs = qs.filter(is_staff=False)
        return qs


