from django.db import models

class Token(models.Model):
    user_id = models.CharField(max_length=40, primary_key=True)
    access_token = models.CharField(max_length=200)
    expires_at = models.DateTimeField()
