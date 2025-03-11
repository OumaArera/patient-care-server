from django.db import models # type: ignore

from custom_admin.models.patient import Patient
from users.models import User

class Vital(models.Model):
    """Create vitals"""
    vitalId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
      Patient,
      on_delete=models.CASCADE,
      related_name='vitals'
    )
    careGiver =  models.ForeignKey(
      User,
      default=None,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='vitals'
    )
    bloodPressure = models.CharField(max_length=100)
    temperature = models.FloatField()
    pulse = models.FloatField()
    oxygenSaturation = models.FloatField()
    pain = models.TextField(null=True, blank=True, default=None)
    dateTaken = models.DateTimeField()
    reasonEdited = models.TextField(null=True, blank=True, default=None)
    reasonFilledLate = models.TextField(null=True, blank=True, default=None)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('updated', 'Updated')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    declineReason = models.TextField(null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_vital(cls, validated_data):
        """
        Create a new vital instance from validated data.
        """
        new_vital = cls(**validated_data)
        return new_vital

