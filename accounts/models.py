from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


class Profile(models.Model):
    ROLE_CHOICES = (
        ('provider', 'Service Provider'),
        ('seeker', 'Service Seeker'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='seeker')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
