from django.db import models
from users.models import User


class Leave(models.Model):
    """Leave management"""

    leaveId = models.AutoField(primary_key=True)
    staff =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='leaves'
    )
    reasonForLeave = models.TextField(null=True, blank=True, default=None)
    startDate = models.DateField()
    endDate = models.DateField()
    STATUS_CHOICES = [
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('pending', 'Pending')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    declineReason = models.TextField(null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_leave(cls, validated_data):
        """
        Create a new leave instance from validated data.
        """
        new_leave = cls(**validated_data)
        return new_leave