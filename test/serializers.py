from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from rest_framework import serializers

from test.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

GENRE_CHOICES=(
    ("TR", "Thriller"),
    ("RO", "Romantic"),
    ("AC", "Action"),
    ("CR", "Crime"),
    ("HO", "Horror"),
)

class MovieSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    start_date = serializers.DateField()
    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default="AC",
    )
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        model = Movie
        fields = ['title', 'description', 'genre', 'start_date','user']

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=300)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, val):
        return make_password(val)
