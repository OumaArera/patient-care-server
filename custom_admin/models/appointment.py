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
    dateTaken = models.DateField()
    details = models.TextField(null=True, blank=True)
    TYPE_CHOICES = [
        ('Primary Care Provider (PCP)', 'Primary Care Provider (PCP)'),
        ('Mental Health Provider / Physician/ Prescriber', 'Mental Health Provider / Physician/ Prescriber'),
        ('Clinician', 'Clinician'),
        ("Peer Support Counsellor", "Peer Support Counsellor"),
        ("Counsellor", "Counsellor"),
        ("Dentist", "Dentist"),
        ("Specialist", "Specialist"),
        ("Other", "Other")
    ]
    type = models.CharField(max_length=200, choices=TYPE_CHOICES)
    nextAppointmentDate = models.DateField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_appointment(cls, validated_data):
        """
        Create a new appointment instance from validated data.
        """
        new_appointment = cls(**validated_data)
        return new_appointment

