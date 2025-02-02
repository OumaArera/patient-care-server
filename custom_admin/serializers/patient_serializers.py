from custom_admin.models.branch import Branch
from custom_admin.models.patient import Patient
from rest_framework import serializers  # type: ignore
from datetime import date


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for creating a Patient."""
    middleNames = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    dateOfBirth = serializers.DateField()
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=True)

    def validate_dateOfBirth(self, value):
        """Ensure the patient is not older than 120 years."""
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age > 120:
            raise serializers.ValidationError("Age cannot be greater than 120 years.")
        return value

    class Meta:
        model = Patient
        fields = [
            "patientId", "firstName", "middleNames", "lastName", "dateOfBirth",
            "diagnosis", "allergies", "physicianName", "pcpOrDoctor", "branch", "room", "cart"
        ]
        read_only_fields = ["patientId"]



class PatientUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Patient."""
    middleNames = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    firstName = serializers.CharField(required=False)
    lastName = serializers.CharField(required=False)
    diagnosis = serializers.CharField(required=False)
    allergies = serializers.CharField(required=False)
    physicianName = serializers.CharField(required=False)
    pcpOrDoctor = serializers.CharField(required=False)
    room = serializers.CharField(required=False)
    cart = serializers.CharField(required=False)
    dateOfBirth = serializers.DateField(required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)

    def validate_dateOfBirth(self, value):
        """Ensure the patient is not older than 120 years."""
        if value:
            today = date.today()
            age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if age > 120:
                raise serializers.ValidationError("Age cannot be greater than 120 years.")
        return value

    class Meta:
        model = Patient
        fields = [
            "firstName", "middleNames", "lastName", "dateOfBirth",
            "diagnosis", "allergies", "physicianName", "pcpOrDoctor", "branch", "room", "cart"
        ]
        extra_kwargs = {field: {"required": False} for field in fields}