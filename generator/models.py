from django.db import models
from django.utils import timezone

class PasswordHistory(models.Model):
    password = models.CharField(max_length=100)
    length = models.IntegerField()
    has_uppercase = models.BooleanField(default=True)
    has_lowercase = models.BooleanField(default=True)
    has_digits = models.BooleanField(default=True)
    has_special = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        # Using MongoDB's native indexing
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Password (ID: {self.id}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"