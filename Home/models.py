from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
# Create your models here.

# feedback model
class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.feed[:50]
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} Profile'
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
    