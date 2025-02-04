from django.db import models # type: ignore

from custom_admin.models.medication import Medication
from custom_admin.models.patient import Patient
from users.models import User  # type: ignore

class MedicationAdministration(models.Model):
    """Create medication administrations"""
    medicationAdministrationId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='medication_ad'
	)
    medication =  models.ForeignKey(
		Medication,
		on_delete=models.CASCADE,
		related_name='medication_ad'
	)
    careGiver =  models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='medication_ad'
	)
    timeAdministered = models.TimeField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('approved', 'Approved')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    reasonNotFiled = models.TextField(blank=True, null=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_administration_medication(cls, validated_data):
        """
        Create a new medication administration instance from validated data.
        """
        new_medication_admin = cls(**validated_data)
        return new_medication_admin

