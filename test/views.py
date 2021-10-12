from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND, OK
from django.http import *
from rest_framework import views, viewsets
from rest_framework.decorators import action, api_view
from .models import *
from .serializers import *
from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from test.pagination import StandardResultsSetPagination


class MovieViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class= StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre']
    search_fields = ['genre']

    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
       comments = Movie.objects.get(id=pk).comments.all()
       return Response(CommentSerializer(comments, many=True).data, status=OK)

    @action(methods=['get'], detail=True)
    def likes(self, request, pk):
       likes = Movie.objects.get(id=pk).reactions.filter(reaction=True)
       return Response(likes.count(), status=OK)   

    @action(methods=['get'], detail=True)
    def dislikes(self, request, pk):
       dislikes = Movie.objects.get(id=pk).reactions.filter(reaction=False)
       return Response(dislikes.count(), status=OK)     


class AuthViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(http_method_names=['post'])
def handle_reaction(request, pk):

    if not request.user.is_authenticated:
        return Response('User is not authenticated!', status=BAD_REQUEST)

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


@api_view(http_method_names=['post'])
def handle_comment_reaction(request, pk):

    if not request.user.is_authenticated:
        return Response('User is not authenticated!', status=BAD_REQUEST)

    try:
        Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return Response('Non existing Comment!', status=NOT_FOUND)

    try:
        reaction = CommentReaction.objects.get(user_id=request.data.get('user'), comment_id=pk)

        reaction.reaction = not reaction.reaction
        reaction.save()

        return Response(CommentReactionSerializer(reaction).data, status=OK)

    except CommentReaction.DoesNotExist:
        reaction = CommentReaction.objects.create(
            user_id=request.data.get('user'), comment_id=pk, reaction=request.data.get('reaction'))

        return Response(CommentReactionSerializer(reaction).data, status=OK)

    except Exception as e:
        raise e    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
     