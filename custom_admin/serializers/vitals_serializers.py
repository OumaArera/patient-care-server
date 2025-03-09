from rest_framework import serializers
from custom_admin.models.vitals import Vital
from custom_admin.models.patient import Patient

class VitalSerializer(serializers.ModelSerializer):
    """Serializer for creating a Vital instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    bloodPressure = serializers.CharField(max_length=100)
    temperature = serializers.FloatField()
    pulse = serializers.FloatField()
    oxygenSaturation = serializers.FloatField()
    pain = serializers.CharField(allow_blank=True, required=False)
    dateTaken = serializers.DateTimeField()
    
    class Meta:
        model = Vital
        fields = [
            "vitalId", "patient", "bloodPressure", "temperature", "pulse", 
            "oxygenSaturation", "pain", "dateTaken", "createdAt", "modifiedAt"
        ]
        read_only_fields = ["vitalId", "createdAt", "modifiedAt"]
    
    def validate(self, data):
        """Ensure that a patient does not have another vital entry for the same date."""
        patient = data.get("patient")
        date_taken = data.get("dateTaken")
        
        # Convert to a date-only format (ignoring time)
        date_only = date_taken.date()
        
        # Check if an entry already exists for the same date
        existing_vital = Vital.objects.filter(
            patient=patient,
            dateTaken__date=date_only
        ).exists()
        
        if existing_vital:
            raise serializers.ValidationError({
                "dateTaken": "A vital entry already exists for this resident on the selected date."
            })
        
        return data

class VitalUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a Vital instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    bloodPressure = serializers.CharField(max_length=100, required=False)
    temperature = serializers.FloatField(required=False)
    pulse = serializers.FloatField(required=False)
    oxygenSaturation = serializers.FloatField(required=False)
    pain = serializers.CharField(allow_blank=True, required=False)
    dateTaken = serializers.DateTimeField(required=False)
    reasonEdited = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model = Vital
        fields = ["patient", "bloodPressure", "temperature", "pulse", "oxygenSaturation", "pain", "dateTaken", "reasonEdited"]
