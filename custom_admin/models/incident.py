from django.db import models
from users.models import User


class Incident(models.Model):
    """Incident reporting"""
    incidentId = models.AutoField(primary_key=True)
    staff =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='incidents'
    )
    filePath = models.FilePathField()
    details = models.TextField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('updated', 'Updated'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_incident(cls, validated_data):
        """
        Create a new incident instance from validated data.
        """
        new_incident = cls(**validated_data)
        return new_incident