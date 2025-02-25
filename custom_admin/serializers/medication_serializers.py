from core.utils.non_empty_validator import MedicationTimeValidator
from custom_admin.models.medication import Medication
from custom_admin.models.patient import Patient
from rest_framework import serializers  # type: ignore

class MedicationSerializer(serializers.ModelSerializer):
    """Serializer for the Medication model."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    medicationName = serializers.CharField(max_length=255)
    medicationCode = serializers.CharField(max_length=50)
    equivalentTo = serializers.CharField(max_length=255)
    instructions = serializers.CharField()
    quantity = serializers.CharField(max_length=255)
    diagnosis = serializers.CharField()
    medicationTime = serializers.ListField(validators=[MedicationTimeValidator()])

    class Meta:
        model = Medication
        fields = [
            "patient", "medicationName", "medicationCode", "equivalentTo",
            "instructions", "quantity", "diagnosis", "medicationTime", 
        ]
        read_only_fields = ["status",  "createdAt", "modifiedAt"]


class MedicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the Medication model."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    medicationName = serializers.CharField(max_length=255, required=False)
    medicationCode = serializers.CharField(max_length=50, required=False)
    equivalentTo = serializers.CharField(max_length=255, required=False)
    instructions = serializers.CharField(required=False)
    quantity = serializers.CharField(max_length=255, required=False)
    diagnosis = serializers.CharField(required=False)
    medicationTime = serializers.ListField(validators=[MedicationTimeValidator()], required=False)
    status = serializers.ChoiceField(required=False, choices=['removed', 'paused', 'active'])

    class Meta:
        model = Medication
        fields = [
            "medicationName", "medicationCode", "equivalentTo", "patient",
            "instructions", "quantity", "diagnosis", "medicationTime", "status"
        ]
        
        