from django.db import models
from user.models import Creator
from django.utils import timezone
# Create your models here.

class Story(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name="stories")
    content = models.FileField(upload_to="stories/", blank=True, null=True)
    text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Story by {self.creator.user.username} at {self.created_at}"

    def is_expired(self):
        return (timezone.now() - self.created_at).total_seconds() > 24 * 60 * 60
