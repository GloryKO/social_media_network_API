from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from .models import Notification

class NotificationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpass',
        )
        self.other_user = get_user_model().objects.create_user(
            email='otheruser@example.com',
            password='otherpass',
        )
        self.notification = Notification.objects.create(
            user=self.user,
            message='You have a new notification.',
            is_read=False,
        )

    def test_unauthenticated_user_cannot_access_notifications(self):
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_access_notifications(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('notification-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming one notification is created for the user

    def test_mark_notification_as_read(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('mark-notification-read', kwargs={'pk': self.notification.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Notification.objects.get(id=self.notification.id).is_read)

    def test_unauthenticated_user_cannot_mark_notification_as_read(self):
        url = reverse('mark-notification-read', kwargs={'pk': self.notification.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Notification.objects.get(id=self.notification.id).is_read)
