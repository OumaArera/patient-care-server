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
		on_delete=models.CASCADE,
		related_name='charts'
	)
    behaviors = models.JSONField()
    behaviorsDescription = models.JSONField(
      default=list,
      blank=True,
      null=True
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('approved', 'Approved')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    reasonNotFiled = models.TextField(blank=True, null=True, default=None)
    dateTaken = models.DateTimeField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_chart(cls, validated_data):
        """
        Create a new charts instance from validated data.
        """
        new_chart = cls(**validated_data)
        return new_chart

