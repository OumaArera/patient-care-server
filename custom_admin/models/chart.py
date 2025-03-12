from django.db import models # type: ignore

from custom_admin.models.patient import Patient
from users.models import User  # type: ignore

class Chart(models.Model):
    """Create charts"""
    chartId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
      Patient,
      on_delete=models.CASCADE,
      related_name='charts'
    )
    careGiver =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='charts'
    )
    behaviors = models.JSONField()
    behaviorsDescription = models.JSONField(
      default=list,
      blank=True,
      null=True
    )
    vitals = models.JSONField(
      default=list,
      blank=True,
      null=True)
    dateTaken = models.DateTimeField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('updated', 'Updated')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")
    declineReason = models.TextField(null=True, blank=True, default=None)
    reasonEdited = models.TextField(null=True, blank=True, default=None)
    reasonFilledLate = models.TextField(null=True, blank=True, default=None)
    reasonNotFilled = models.TextField(null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
      unique_together = ('patient', 'dateTaken') 

    @classmethod
    def create_chart(cls, validated_data):
        """
        Create a new charts instance from validated data.
        """
        new_chart = cls(**validated_data)
        return new_chart

