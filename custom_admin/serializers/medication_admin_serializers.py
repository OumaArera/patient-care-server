from django.utils.timezone import timedelta
from rest_framework import serializers
from custom_admin.models.medical_administration import MedicationAdministration
from custom_admin.models.medication import Medication
from custom_admin.models.patient import Patient


class MedicationAdministrationSerializer(serializers.ModelSerializer):
    """Serializer for creating MedicationAdministration records."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())
    timeAdministered = serializers.DateTimeField(required=True)

    class Meta:
        model = MedicationAdministration
        fields = [
            "medicationAdministrationId", "patient", "medication",
            "timeAdministered", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["medicationAdministrationId",  "createdAt", "modifiedAt"]



class MedicationAdministrationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating MedicationAdministration records."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), required=False)
    timeAdministered = serializers.DateTimeField(required=False)
    

    class Meta:
        model = MedicationAdministration
        fields = [
            "patient", "medication", "timeAdministered"
        ]
