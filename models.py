from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # Preferences
    preferred_timezone = models.CharField(max_length=50, default='UTC')
    preferred_weather_unit = models.CharField(
        max_length=10, 
        choices=[('metric', 'Celsius'), ('imperial', 'Fahrenheit')],
        default='metric'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()
    
    def save(self, *args, **kwargs):
        """Override save method to resize avatar images"""
        super().save(*args, **kwargs)
        
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.avatar.path)
            except Exception:
                pass  # Handle cases where image processing fails


class UserProfile(models.Model):
    """Extended user profile information"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    task_reminders = models.BooleanField(default=True)
    news_digest = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

