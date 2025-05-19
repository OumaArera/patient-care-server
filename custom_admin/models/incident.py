from django.db import models
from users.models import User
from datetime import timedelta
from django.utils import timezone

class Incident(models.Model):
    """Incident reporting"""
    incidentId = models.AutoField(primary_key=True)
    raisedBy = models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='incident_raised_by'
    )
    assignedTo =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='incident_assigned_to'
    )
    incident = models.TextField(default=list)
    type = models.CharField(max_length=255)
    comments = models.JSONField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="low")
    resolvedAt = models.DateTimeField(null=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_incident(cls, validated_data):
        """
        Create a new incident instance from validated data.
        Automatically set resolvedAt to 12 hours from now if not provided.
        """
        if 'resolvedAt' not in validated_data or validated_data['resolvedAt'] is None:
            validated_data['resolvedAt'] = timezone.now() + timedelta(hours=12)
        return cls.objects.create(**validated_data)