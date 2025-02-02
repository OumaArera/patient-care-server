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
    medicationTime = serializers.TimeField()

    class Meta:
        model = Medication
        fields = [
            "patient", "medicationName", "medicationCode", "equivalentTo",
            "instructions", "quantity", "diagnosis", "medicationTime", 
        ]


class MedicationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the Medication model."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    medicationName = serializers.CharField(max_length=255, required=False)
    medicationCode = serializers.CharField(max_length=50, required=False)
    equivalentTo = serializers.CharField(max_length=255, required=False)
    instructions = serializers.CharField(required=False)
    quantity = serializers.CharField(max_length=255, required=False)
    diagnosis = serializers.CharField(required=False)
    medicationTime = serializers.TimeField(required=False)

    class Meta:
        model = Medication
        fields = [
            "medicationName", "medicationCode", "equivalentTo", "patient",
            "instructions", "quantity", "diagnosis", "medicationTime", 
        ]