from rest_framework import serializers  # type: ignore

class NonEmptyListValidator:
    """Validator to ensure JSON fields contain a non-empty list of dictionaries."""
    
    def __call__(self, value):
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise serializers.ValidationError("This field must be a list of dictionaries.")
        if not value:
            raise serializers.ValidationError("This field cannot be empty.")


class MedicationTimeValidator:
    """
    Validator to check that medicationTime is not an empty list.
    """
    def __call__(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("medicationTime must be a list.")
        if not value:
            raise serializers.ValidationError("medicationTime cannot be an empty list.")
