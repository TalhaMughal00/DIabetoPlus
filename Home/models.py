from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# feedback modal
class feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.feed[:50]