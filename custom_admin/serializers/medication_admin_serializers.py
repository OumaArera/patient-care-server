from datetime import datetime, timedelta
from django.utils.timezone import localtime # type: ignore
from custom_admin.models.medical_administration import MedicationAdministration
from custom_admin.models.medication import Medication
from custom_admin.models.patient import Patient
from rest_framework import serializers  # type: ignore


class MedicationAdministrationSerializer(serializers.ModelSerializer):
    """Serializer for creating MedicationAdministration records."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())
    timeAdministered = serializers.TimeField()

    class Meta:
        model = MedicationAdministration
        fields = [
            "medicationAdministrationId", "patient", "medication",
            "timeAdministered", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["medicationAdministrationId", "createdAt", "modifiedAt"]

    def validate(self, data):
        """Ensure no other medication was administered for the same patient within 4 hours."""
        patient = data.get("patient")
        medication = data.get("medication")
        time_administered = data.get("timeAdministered")
        today = localtime().date()

        min_time = (datetime.combine(
            today, 
            time_administered
            ) - timedelta(
                hours=4
            )).time()

        conflicting_medication = MedicationAdministration.objects.filter(
            patient=patient,
            medication=medication,
            createdAt__date=today,
            timeAdministered__gte=min_time,
        ).exclude(
            medicationAdministrationId=self.instance.medicationAdministrationId\
                if self.instance else None
        )

        if conflicting_medication.exists():
            raise serializers.ValidationError(
                "Another medication has already been administered to this patient within the last 4 hours."
            )

        return data



class MedicationAdministrationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating MedicationAdministration records."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), required=False)
    timeAdministered = serializers.TimeField(required=False)

    class Meta:
        model = MedicationAdministration
        fields = [
            "patient", "medication", "timeAdministered"
        ]
