from django.utils.timezone import timedelta
from django.utils.timezone import now
from rest_framework import serializers
from custom_admin.models.medical_administration import MedicationAdministration
from custom_admin.models.medication import Medication
from custom_admin.models.patient import Patient


class MedicationAdministrationSerializer(serializers.ModelSerializer):
    """Serializer for creating MedicationAdministration records."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())
    timeAdministered = serializers.DateTimeField(required=True)
    status = serializers.ChoiceField(required=True, choices=['removed', 'paused', 'active'])

    class Meta:
        model = MedicationAdministration
        fields = [
            "medicationAdministrationId", "patient", "medication",
            "timeAdministered", "createdAt", "modifiedAt", "status"
        ]
        read_only_fields = ["medicationAdministrationId", "createdAt", "modifiedAt"]

    def validate(self, data):
        """Ensure no duplicate medication administration within 1 hour."""
        patient = data.get("patient")
        medication = data.get("medication")
        time_administered = data.get("timeAdministered")

        # Define the time window (+/- 1 hour)
        time_lower_bound = time_administered - timedelta(hours=1)
        time_upper_bound = time_administered + timedelta(hours=1)

        # Check if another record exists within this time frame
        conflicting_entry = MedicationAdministration.objects.filter(
            patient=patient,
            medication=medication,
            timeAdministered__range=(time_lower_bound, time_upper_bound),
        )

        # Exclude current instance if updating
        if self.instance:
            conflicting_entry = conflicting_entry.exclude(pk=self.instance.pk)

        if conflicting_entry.exists():
            raise serializers.ValidationError(
                "A medication administration record for this resident and medication "
                "already exists within one hour of the specified time."
            )

        return data



class MedicationAdministrationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating MedicationAdministration records."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all(), required=False)
    timeAdministered = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(required=False, choices=['removed', 'paused', 'active'])

    class Meta:
        model = MedicationAdministration
        fields = [
            "patient", "medication", "timeAdministered", "status"
        ]
