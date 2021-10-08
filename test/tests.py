from django.http.response import ResponseHeaders
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from test.models import *
from rest_framework import status
from test.serializers import *
from unittest.mock import patch


class MovieTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='test')

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.crime_movie = Movie.objects.create(title='CRIME MOVIE', description='desc', start_date='2007-10-8',
                                                genre='CR', user=self.user)
        self.thriller_movie = Movie.objects.create(title='THRILLER MOVIE', description='desc', start_date='2007-10-8',
                                                   genre='TR', user=self.user)

    def test_addMovie(self):
        with patch('test.models.send_mail_async') as sendMail_mock:
            response = self.client.post('/movies/', {'title': 'TEST MOVIE', 'description': 'desc', 'start_date': '2007-10-8',
                                                    'genre': 'TR', 'user': f'{self.user.id}'}, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            sendMail_mock(response.data.get('id'))
            self.assertTrue(sendMail_mock.called)

    def test_getAllMovies(self):
        response = self.client.get('/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Movie.objects.count())

    def test_searchCrimeMovies(self):
        response = self.client.get('/movies/?search=CR', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         Movie.objects.filter(genre='CR').count())

    def test_filterThrillereMovies(self):
        response = self.client.get('/movies/?genre=TR', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),
                         Movie.objects.filter(genre='TR').count())

    def test_updateMovie(self):
        self.thriller_movie.title = 'CHANGE'
        serializer = MovieSerializer(self.thriller_movie)

        response = self.client.put(
            f'/movies/{self.thriller_movie.id}/', serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), 'CHANGE')

    def test_deleteMovie(self):
        get_response = self.client.get(f'/movies/{self.thriller_movie.id}/')
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)

        delete_response = self.client.delete(
            f'/movies/{self.thriller_movie.id}/')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_204_NO_CONTENT)

        get_response = self.client.get(f'/movies/{self.thriller_movie.id}/')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deleteMovie_fail(self):
        delete_response = self.client.delete('/movies/77777/')
        self.assertEqual(delete_response.status_code,
                         status.HTTP_404_NOT_FOUND)


class ReactionTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user', password='test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.crime_movie = Movie.objects.create(title='CRIME MOVIE', description='desc', start_date='2007-10-8',
                                                genre='CR', user=self.user)
        self.thriller_movie = Movie.objects.create(title='THRILLER MOVIE', description='desc', start_date='2007-10-8',
                                                   genre='TR', user=self.user)

        self.reaction = Reaction.objects.create(
            user=self.user, movie=self.crime_movie, reaction='True')

    def test_addReaction_fail(self):
        response = self.client.post(f'/movies/7777/reactions/',
                                    {'user': '1', 'movie': '7777', 'reaction': 'True'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_addReaction(self):

        reaction = {
            'user': self.user.id,
            'movie': self.thriller_movie.id,
            'reaction': 'True'
        }

        response = self.client.post(
            f'/movies/{self.thriller_movie.id}/reactions/', reaction, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_updateReaction(self):
        self.reaction.reaction = 'False'
        serializer = ReactionSerializer(self.reaction)

        response = self.client.post(
            f'/movies/{self.reaction.movie.id}/reactions/', serializer.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get('reaction'))

class UserTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_addUser(self):    
        response = self.client.post('/users/', {'username': 'test_user_2', 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.login(username='test_user_2', password='test')

    def test_logIn(self):    
        response = self.client.post('/users/', {'username': 'test_user_2', 'password': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.login(username='test_user_2', password='test')
        self.assertTrue(response)