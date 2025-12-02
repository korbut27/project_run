from django.contrib.auth.models import User
from rest_framework import viewsets, status
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
    queryset = Run.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RunWriteSerializer
        return RunReadSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        run = serializer.save()

        # Сериализация сохраненного объекта с помощью RunReadSerializer
        read_serializer = RunReadSerializer(run, context={'request': request})
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

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


