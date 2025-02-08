from django.db import models 
from custom_admin.models.patient import Patient
from users.models import User  

class PatientManager(models.Model):
    """Create PatientManager"""
    patientManagerId = models.AutoField(primary_key=True)
    patient =  models.ForeignKey(
      Patient,
      on_delete=models.CASCADE,
      related_name='patient_managers'
    )
    careGiver =  models.ForeignKey(
      User,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='patient_managers'
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    class Meta:
      unique_together = ('patient', 'careGiver') 

    @classmethod
    def create_patient_manager(cls, validated_data):
        """
        Create a new patient managers instance from validated data.
        """
        new_patient_manager = cls(**validated_data)
        return new_patient_manager

