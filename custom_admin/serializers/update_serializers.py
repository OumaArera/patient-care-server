from datetime import timedelta
from rest_framework import serializers
from custom_admin.models.update import Update
from custom_admin.models.patient import Patient

class UpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating an Update instance."""
    
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
    notes = serializers.CharField()
    dateTaken = serializers.DateField()
    type = serializers.ChoiceField(required=True, choices=['weekly', 'monthly'])
    weight = serializers.IntegerField(min_value=0, required=False)
    weightDeviation = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Update
        fields = [
            "updateId", "patient", "notes", "dateTaken", "weight", "type", "weightDeviation",
            "createdAt", "modifiedAt"
        ]
        read_only_fields = ["updateId", "createdAt", "modifiedAt", "weightDeviation"]

    def validate(self, data):
        """Perform validation and assign computed values where necessary."""
        patient = data.get("patient")
        date_taken = data.get("dateTaken")
        update_type = data.get("type")
        weight = data.get("weight")

        if update_type == "weekly":
            # Weekly updates: weight and weightDeviation should not be required
            data.pop("weight", None)  # Remove weight if provided
            data.pop("weightDeviation", None)  # Remove weightDeviation if provided

        elif update_type == "monthly":
            if weight is None:
                raise serializers.ValidationError({"weight": "Weight is required for monthly updates."})

            # Get the most recent monthly update within the last month for the same patient
            one_month_ago = date_taken - timedelta(days=30)
            last_monthly_update = (
                Update.objects.filter(patient=patient, type="monthly", dateTaken__gte=one_month_ago)
                .exclude(dateTaken=date_taken)  # Exclude the current update
                .order_by("-dateTaken")
                .first()
            )

            if last_monthly_update and last_monthly_update.weight is not None:
                data["weightDeviation"] = weight - last_monthly_update.weight
            else:
                data["weightDeviation"] = 0  # No previous data, deviation is 0

        return data



class UpdateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an Update instance."""
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), required=False)
    notes = serializers.CharField(required=False)
    dateTaken = serializers.DateField(required=False)
    status = serializers.ChoiceField(required=False, choices=['pending', 'declined', 'approved'])
    type = serializers.ChoiceField(required=False, choices=['weekly', 'monthly'])
    weight = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = Update
        fields = [
            "patient", "notes", "dateTaken", "status", "weight", "type"
        ]
