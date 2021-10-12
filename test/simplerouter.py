from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
router.register(r'users', AuthViewSet)
router.register(r'comments', CommentViewSet)
