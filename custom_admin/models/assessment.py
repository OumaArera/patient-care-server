from django.db import models
from custom_admin.models.patient import Patient


class Assessment(models.Model):
    """Assessment scheduling"""
    assessmentId = models.AutoField(primary_key=True)
    resident =  models.ForeignKey(
      Patient,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='assessments'
    )
    assessmentStartDate = models.DateField(null=True, default=None)
    assessmentNextDate = models.DateField(null=True, default=None)
    NCPStartDate = models.DateField(null=True, default=None)
    NCPNextDate = models.DateField(null=True, default=None)
    socialWorker = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_assessment(cls, validated_data):
        """
        Create a new assessment instance from validated data.
        """
        new_assessment = cls(**validated_data)
        return new_assessment