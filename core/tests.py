from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse('register')
#create a user  
def create_user(**params):
    return get_user_model().objects.create_user(**params)

#public tests- tests unauthenticated users activities
class publicApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        payload ={
            'name':'testusername',
            'email':'test@example.com',
            'password':'testpass123'
        }

        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertNotIn('password',res.data)