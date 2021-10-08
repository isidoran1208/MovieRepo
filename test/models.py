from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from celery import shared_task

GENRE_CHOICES = (
    ("TR", "Thriller"),
    ("RO", "Romantic"),
    ("AC", "Action"),
    ("HO", "Horror"),
    ("CR", "Crime"),
)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    start_date = models.DateField()
    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default="AC",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def likes(self):
        return self.reactions.likes

    def dislikes(self):
        return self.reactions.dislikes


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


@receiver(post_save, sender=Movie, dispatch_uid="send_mail_movie")
def send_mail_movie(sender, instance, created, **kwargs):
    if created:
        send_mail_async.delay(instance.id)


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="reactions")
    reaction = models.BooleanField(default=False)
