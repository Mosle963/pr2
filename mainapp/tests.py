from django.test import TestCase
from .models import CustomUser

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='test@test.com', password='testpassword')

    def test_valid_login(self):
        login = self.client.login(email='test@test.com', password='testpassword')
        self.assertTrue(login)

    def test_invalid_login(self):
        login = self.client.login(email='test@test.com', password='wrongpassword')
        self.assertFalse(login)
