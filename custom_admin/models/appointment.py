from django.db import models

from custom_admin.models.patient import Patient

class Appointment(models.Model):
    """Create appointments"""
    appointmentId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
		Patient,
		on_delete=models.CASCADE,
		related_name='appointments'
	)
    weeklyAppointments = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    fortnightAppointments = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    monthlyAppointments = models.JSONField(
        default=list,
        blank=True,
        null=True
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_appointment(cls, validated_data):
        """
        Create a new appointment instance from validated data.
        """
        new_appointment = cls(**validated_data)
        return new_appointment

