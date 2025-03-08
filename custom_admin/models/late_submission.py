from django.db import models # type: ignore

from custom_admin.models.patient import Patient
from users.models import User  # type: ignore

class LateSubmission(models.Model):
    """Create late submission"""
    lateSubmissionId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
      Patient,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='late_submissions'
    )
    manager = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='manager_late_submissions'
    )
    careGiver = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='caregiver_late_submissions'
    )
    TYPE_CHOICES = [
        ('charts', 'Charts'),
        ('medication', 'Medication'),
        ('updates', 'Updates'),
        ('vital', 'Vital')
    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    start = models.DateTimeField()
    duration = models.FloatField()
    reasonForLateSubmission = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_late_submission(cls, validated_data):
        """
        Create a new late submision instance from validated data.
        """
        new_submission = cls(**validated_data)
        return new_submission

