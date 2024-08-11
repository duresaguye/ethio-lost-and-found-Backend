from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class Item(models.Model):
    ITEM_TYPE_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact = models.CharField(max_length=100, default='N/A')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='items')
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
