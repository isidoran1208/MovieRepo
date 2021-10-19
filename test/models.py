from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery import shared_task
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes

import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict


GENRE_CHOICES = (
    ("TR", "Thriller"),
    ("RO", "Romantic"),
    ("AC", "Action"),
    ("HO", "Horror"),
    ("CR", "Crime"),
)


@parser_classes((MultiPartParser, ))
class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    start_date = models.DateField()
    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default="AC",
    )
    photo = models.ImageField(upload_to='movie_imgs', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

@shared_task
def send_mail_async(id):
    movie = Movie.objects.get(id=id)
    send_mail(
        'Movie',
        'Movie "' + movie.title + '" has been created',
        None,
        ['1ee1484e54-3e2f9a@inbox.mailtrap.io'],
        fail_silently=False,
    )

@receiver(post_save, sender=Movie)
def notify_new_movie(sender, instance, created, **kwargs):
    if created:
        send_mail_async.delay(instance.id)


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.BooleanField(default=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=500)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


@receiver(post_save, sender=Movie)
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=Reaction)
def notify_new_movie(sender, instance, created, **kwargs):
    if created:
        send_mail_async.delay(instance.id)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            type(instance).__name__,
            {
                "type": f"new.{type(instance).__name__}",
                "data": json.dumps(model_to_dict(instance), indent=4, sort_keys=True, default=str)
            }
        )


class CommentReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.BooleanField(default=False)    