from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from rest_framework import serializers

from test.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class MovieSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    start_date = serializers.DateField()
    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default="AC",
    )
    photo = models.ImageField(upload_to='movie_imgs', null=True)
    user = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'genre', 'start_date', 'photo', 'user']


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=300)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_password(self, val):
        return make_password(val)


class ReactionSerializer(serializers.ModelSerializer):
    user = ForeignKey(User, on_delete=CASCADE)
    movie = ForeignKey(Movie, on_delete=CASCADE)
    reaction = models.BooleanField(default=False)

    class Meta:
        model = Reaction
        fields = ['user', 'movie', 'reaction']
