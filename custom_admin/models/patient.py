from django.db import models # type: ignore

from custom_admin.models.branch import Branch  # type: ignore

class Patient(models.Model):
    """Create patients"""
    patientId = models.AutoField(primary_key=True)
    avatar = models.FileField(null=True, blank=True, upload_to="patients", default=None)
    firstName = models.CharField(max_length=255)
    middleNames = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255)
    dateOfBirth = models.DateField()
    diagnosis = models.TextField()
    allergies = models.TextField()
    physicianName = models.CharField(max_length=255)
    pcpOrDoctor = models.CharField(max_length=255)
    branch = models.ForeignKey(
		Branch,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='patients'
	)
    room = models.CharField(max_length=255)
    cart = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_patient(cls, validated_data):
        """
        Create a new patients instance from validated data.
        """
        new_patient = cls(**validated_data)
        return new_patient

