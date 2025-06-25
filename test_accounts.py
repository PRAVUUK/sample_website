from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from accounts.models import User
from accounts.forms import UserRegistrationForm, UserProfileForm

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }
    
    def test_create_user(self):
        """Test user creation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test superuser creation"""
        user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_user_full_name(self):
        """Test user full name property"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.get_full_name(), 'Test User')
    
    def test_unique_username(self):
        """Test username uniqueness"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(**self.user_data)
    
    def test_unique_email(self):
        """Test email uniqueness"""
        User.objects.create_user(**self.user_data)
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'testuser2'
        with self.assertRaises(Exception):
            User.objects.create_user(**duplicate_data)


class UserRegistrationFormTest(TestCase):
    """Test cases for UserRegistrationForm"""
    
    def test_valid_form(self):
        """Test form with valid data"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'timezone': 'UTC'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test form with mismatched passwords"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'timezone': 'UTC'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_duplicate_username(self):
        """Test form with duplicate username"""
        User.objects.create_user(
            username='testuser',
            email='existing@example.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'timezone': 'UTC'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class AuthenticationViewsTest(TestCase):
    """Test cases for authentication views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')
    
    def test_login_view_post_valid(self):
        """Test login view POST with valid credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
    
    def test_login_view_post_invalid(self):
        """Test login view POST with invalid credentials"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please enter a correct username and password')
    
    def test_register_view_get(self):
        """Test register view GET request"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
    
    def test_register_view_post_valid(self):
        """Test register view POST with valid data"""
        response = self.client.post(reverse('accounts:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'timezone': 'UTC'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_logout_view(self):
        """Test logout view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_profile_view_unauthenticated(self):
        """Test profile view for unauthenticated user"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_view_unauthenticated(self):
        """Test dashboard view for unauthenticated user"""
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login


class UserProfileTest(TestCase):
    """Test cases for user profile functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_profile_update(self):
        """Test profile update functionality"""
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'timezone': 'America/New_York'
        })
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
    
    def test_settings_view(self):
        """Test settings view"""
        response = self.client.get(reverse('accounts:settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Settings')


class PasswordResetTest(TestCase):
    """Test cases for password reset functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_reset_view(self):
        """Test password reset view"""
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reset Password')
    
    def test_password_reset_post(self):
        """Test password reset POST request"""
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after form submission


class IntegrationTest(TestCase):
    """Integration tests for accounts module"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_complete_user_journey(self):
        """Test complete user registration and login journey"""
        # Register new user
        response = self.client.post(reverse('accounts:register'), {
            'username': 'journeyuser',
            'email': 'journey@example.com',
            'first_name': 'Journey',
            'last_name': 'User',
            'password1': 'journeypass123',
            'password2': 'journeypass123',
            'timezone': 'UTC'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verify user was created
        user = User.objects.get(username='journeyuser')
        self.assertEqual(user.email, 'journey@example.com')
        
        # Login with new user
        response = self.client.post(reverse('accounts:login'), {
            'username': 'journeyuser',
            'password': 'journeypass123'
        })
        self.assertEqual(response.status_code, 302)
        
        # Access dashboard
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Update profile
        response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'Updated Journey',
            'last_name': 'User',
            'email': 'journey@example.com',
            'bio': 'Test bio',
            'timezone': 'America/New_York'
        })
        
        # Verify profile update
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Updated Journey')
        
        # Logout
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
        
        # Verify logout by trying to access dashboard
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

