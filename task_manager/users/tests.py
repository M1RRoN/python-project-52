import json
import os

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy

from .forms import UserForm
from .models import CustomUser


class TestUser(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

        # self.user = CustomUser.objects.get(pk=1)
        # self.user2 = CustomUser.objects.get(pk=2)
        self.create_url = reverse_lazy('create_user')
        self.login_url = reverse_lazy('login')
        self.users_url = reverse_lazy('users')
        self.users = get_user_model().objects.all()
        self.user1 = get_user_model().objects.get(pk=1)
        self.user2 = get_user_model().objects.get(pk=2)
        self.update_pk1_url = reverse_lazy('update', kwargs={'pk': 1})
        self.delete_pk1_url = reverse_lazy('delete', kwargs={'pk': 1})
        self.delete_pk2_url = reverse_lazy('delete', kwargs={'pk': 2})
        with open(os.path.join('fixtures', 'test_user.json')) as file:
            self.test_user = json.load(file)

    def test_create_page(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

    def test_create_user(self):
        response = self.client.post(self.create_url, self.test_user)
        # self.assertRedirects(response, self.login_url, 302)
        self.user = get_user_model().objects.get(pk=4)
        self.assertEqual(first=self.user.username, second=self.test_user.get('username'))
        self.assertEqual(first=self.user.first_name, second=self.test_user.get('first_name'))
        self.assertEqual(first=self.user.last_name, second=self.test_user.get('last_name'))

    def test_user_create_form_with_data(self):
        user_form = UserForm(data=self.test_user)
        self.assertTrue(user_form.is_valid())
        self.assertEqual(len(user_form.errors), 0)

    def test_user_creation_form_with_no_data(self):
        user_form = UserForm(data={})
        self.assertFalse(user_form.is_valid())
        self.assertEqual(len(user_form.errors), 3)

    def test_open_update_page(self):
        self.client.force_login(self.user1)
        response = self.client.get(self.update_pk1_url)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        self.client.force_login(self.user1)
        self.assertNotEqual(self.user1.username, self.test_user.get('username'))
        response = self.client.post(self.update_pk1_url, data=self.test_user)
        self.assertEqual(response.status_code, 302)
        self.user1 = get_user_model().objects.get(pk=1)
        self.assertEqual(self.user1.username, self.test_user.get('username'))

    def test_update_other_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.update_pk1_url, data=self.test_user)
        self.assertRedirects(response, self.users_url, 302, 200)

    def test_open_delete_page(self):
        #delete user
        self.client.force_login(self.user1)
        response = self.client.get(self.delete_pk1_url)
        self.assertEqual(response.status_code, 200)
        # delete other user
        self.client.force_login(self.user2)
        response = self.client.get(self.delete_pk1_url)
        self.assertEqual(response.status_code, 302)

    def test_delete_user(self):
        self.client.force_login(self.user2)
        response = self.client.delete(self.delete_pk2_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 2)
        with self.assertRaises(get_user_model().DoesNotExist):
            get_user_model().objects.get(pk=2)

    def test_delete_other_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.delete_pk1_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.users.count(), 3)
