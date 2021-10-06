from django.http import *
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre']
    search_fields = ['genre']

class AuthViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer