from django.db import models
from django.contrib.auth.models import User

class GRecords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mor_fast = models.IntegerField(null=True, blank=True)
    mor_after = models.IntegerField(null=True, blank=True)
    evening = models.IntegerField(null=True, blank=True)
    night_fast = models.IntegerField(null=True, blank=True)
    night_after = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"User ID: {self.user.id} - {self.date}"
