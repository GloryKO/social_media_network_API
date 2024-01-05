from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

CREATE_USER_URL = reverse('register')
CREATE_TOKEN_URL = reverse('user_token')
MANAGE_USER_URL = reverse('profile')
#create a user  
def create_user(**params):
    return get_user_model().objects.create_user(**params)


class publicApiTests(TestCase):
    """This class contains Tests Unathenticated Users activities """
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_success(self):
        """Test User creation is successful"""
        payload ={
            'name':'testusername',
            'email':'test@example.com',
            'password':'testpass123'
        }

        res=self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertNotIn('password',res.data)
  
    def test_user_exists(self):
        """Test User is already exists """
        payload = {
             'name':'testusername',
            'email':'test@example.com',
            'password':'testpass123'
        }
        create_user(**payload)#user is already created here

        res= self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test user token creation """
        payload={
            'name':'testusername',
            'email':'test@example.com',
            'password':'testpass123'
        }
        create_user(**payload)
        res=self.client.post(CREATE_TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('token',res.data)

    def test_create_token_invalid_details(self):
        create_user(email='test@example.com', password='testpass', name='testuser')
        payload ={
            'name':'testusername',
            'email':'test@example.com',
            'password':'testpass123'
        }
        res = self.client.post(CREATE_TOKEN_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token',res.data)

class PrivateApiTest(TestCase):
    def setUp(self):
        self.user =create_user(
            name='testusername',
            email='test@example.com',
            password='testpass123'
            )

        self.client =APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile(self):
        res=self.client.get(MANAGE_USER_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
    
    def test_update_user_profile(self):
        payload = {'name': 'newname', 'password': 'testnewpass'}
        self.client.patch(MANAGE_USER_URL,payload)