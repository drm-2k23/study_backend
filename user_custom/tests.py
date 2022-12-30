from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from product.models import Category
import json


# Create your tests here.
class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        data = {'name': 'varun bhardwaj',
                'email': 'karan@gmail.com',
                'password': '123Varun',
                'password1': '123Varun'}
        user_create = self.client.post('http://127.0.0.1:8000/api/v1/users/create_user/', data,
                                       format='json')
        self.request = self.client.post('http://127.0.0.1:8000/api/token/', {'email': 'karan@gmail.com',
                                                                             'password': '123Varun'},
                                        format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.request.json()["access"])
        create_categories = Category.objects.create(name="Books")
        self.assertEqual(self.request.status_code, status.HTTP_200_OK)
        self.assertEqual(user_create.status_code, status.HTTP_201_CREATED)

    def test_create_account(self):
        categories_obj = self.client.get("http://127.0.0.1:8000/api/v1/products/category_list/")
        self.assertEqual(categories_obj.status_code, status.HTTP_200_OK)

    def test_user_account(self):
        user_detail = self.client.get("http://127.0.0.1:8000/api/v1/users/log_in/")
        self.assertEqual(user_detail.status_code, status.HTTP_200_OK)
