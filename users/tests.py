from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')
ME_URL = reverse('users:me')


class UserTestCase(TestCase):

    def test_create_user_with_email(self):
        """Test for creating user with email"""
        email = 'testuser@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_normalized_email(self):
        """Test if new user email is normalized"""
        email = 'testuser@GMAIL.COM'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating new user with no email raises error"""
        with self.assertRaises(ValueError):
            email = None
            password = 'testpass123'
            get_user_model().objects.create_user(email, password)

    def test_create_new_superuser(self):
        email = 'testsuperuser@gmail.com'
        password = 'testsuperpass123'
        user = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user(self):
        """Test creating user with valid payload"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123',
            'firstname': 'Test',
            'lastname': 'User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.email, payload['email'])
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating a user that already exists"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123'
        }
        get_user_model().objects.create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 chars"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'test',
            'firstname': 'Test',
            'lastname': 'User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123'
        }
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is NOT created if credentials are invalid"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123'
        }
        get_user_model().objects.create_user(**payload)
        payload_test = {
            'email': 'testuser@gmail.com',
            'password': 'wrongpass'
        }
        res = self.client.post(TOKEN_URL, payload_test)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_user_no_token(self):
        """Test that token is NOT created if user doesn't exist"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {
            'email': 'testuser@gmail.com',
            'password': ''
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unathorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        payload = {
            'email': 'testuser@gmail.com',
            'password': 'testpass123',
            'firstname': 'Test',
            'lastname': 'User'
        }
        self.user = get_user_model().objects.create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile(self):
        """Test retrieving profile for loggedIn user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'firstname': self.user.firstname,
            'lastname': self.user.lastname
        })

    def test_post_not_allowed_on_me(self):
        """Test that POST method is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile"""
        payload = {
            'email': 'testusernew@gmail.com',
            'password': 'testpass123new',
            'firstname': 'Test',
            'lastname': 'User'
        }

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.firstname, payload['firstname'])
        self.assertEqual(self.user.lastname, payload['lastname'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
