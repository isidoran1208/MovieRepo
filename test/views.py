from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND, OK
from django.http import *
from rest_framework import views, viewsets
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


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


@api_view(http_method_names=['post'])
def handle_reaction(request, pk):

    try:
        Movie.objects.get(id=pk)
    except Movie.DoesNotExist:
        return Response('Non existing Movie!', status=NOT_FOUND)

    try:
        reaction = Reaction.objects.get(user_id=request.data.get('user'), movie_id=pk)

        reaction.reaction = not reaction.reaction
        reaction.save()

        reaction_string = "liked" if reaction.reaction else "disliked"
        # return Response(f"Reaction updated: movie with id {pk} {reaction_string}.", status=OK)
        return Response(ReactionSerializer(reaction).data, status=OK)

    except Reaction.DoesNotExist:
        reaction = Reaction.objects.create(
            user_id=request.data.get('user'), movie_id=pk, reaction=request.data.get('reaction'))

        reaction_string = "liked" if reaction.reaction else "disliked"
        # return Response(f"Reaction created: movie with id {pk} {reaction_string}.", status=OK)
        return Response(ReactionSerializer(reaction).data, status=OK)

    except Exception as e:
        raise e
