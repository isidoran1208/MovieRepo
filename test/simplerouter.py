from test.consumers import MovieConsumer
from .views import *
from rest_framework import routers

from django.urls import path
from . import consumers

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
router.register(r'users', AuthViewSet)
router.register(r'comments', CommentViewSet, basename='Comment')

websocket_urlpatterns = [
    path('ws/movies/', consumers.MovieConsumer.as_asgi()),
    path('ws/comments/', consumers.CommentConsumer.as_asgi()),
    path('ws/reactions/', consumers.ReactionConsumer.as_asgi()),
]
